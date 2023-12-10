import asyncio
import logging

from core.commands.feed import FeedRun
from core.event_decorators import command_handler
from core.events.backtest import BacktestEnded
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_datasource_factory import AbstractDataSourceFactory
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.models.exchange import ExchangeType
from core.models.lookback import Lookback
from core.models.order import OrderType
from core.queries.portfolio import GetTopStrategy

logger = logging.getLogger(__name__)


class Feed(AbstractEventManager):
    def __init__(
        self,
        signal_factory: AbstractSignalActorFactory,
        position_factory: AbstractPositionActorFactory,
        risk_factory: AbstractRiskActorFactory,
        executor_factory: AbstractExecutorActorFactory,
        datasource_factory: AbstractDataSourceFactory,
        config_service: AbstractConfig,
    ):
        super().__init__()
        self.signal_factory = signal_factory
        self.position_factory = position_factory
        self.risk_factory = risk_factory
        self.executor_factory = executor_factory
        self.datasource_factory = datasource_factory
        self.config_service = config_service

    @command_handler(FeedRun)
    async def _feed_handler(self, command: FeedRun):
        logger.info("Run feed")

        strategies = await self.query(
            GetTopStrategy(num=self.config_service.get("system")["active_strategy_num"])
        )

        await asyncio.gather(
            *[
                self._run_trading(command.datasource, symbol, timeframe, strategy)
                for symbol, timeframe, strategy in strategies
            ]
        )

    async def _run_trading(self, ws, symbol, timeframe, strategy):
        logger.info(f"Prefetch data: {symbol}_{timeframe}{strategy}")

        actors = [
            self.signal_factory.create_actor(symbol, timeframe, strategy),
            self.position_factory.create_actor(symbol, timeframe, strategy),
            self.risk_factory.create_actor(symbol, timeframe, strategy),
            self.executor_factory.create_actor(
                OrderType.PAPER,
                symbol,
                timeframe,
                strategy,
            ),
        ]

        datasource = self.datasource_factory.create(
            ExchangeType.BYBIT,
            symbol,
            timeframe,
        )

        iterator = datasource.fetch(
            Lookback.ONE_MONTH, None, self.config_service.get("backtest")["batch_size"]
        )

        async for bar in iterator:
            await self.dispatch(
                NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
            )

        last_bar = iterator.get_last_bar()

        if last_bar:
            await self.dispatch(
                BacktestEnded(symbol, timeframe, strategy, last_bar.ohlcv.close)
            )

        actors[-1].stop()

        logger.info(f"Start trading: {symbol}_{timeframe}{strategy}")

        actors[-1] = self.executor_factory.create_actor(
            OrderType.MARKET
            if self.config_service.get("system")["mode"] == 1
            else OrderType.PAPER,
            symbol,
            timeframe,
            strategy,
        )

        ws_datasource = self.datasource_factory.create(
            ws,
            symbol,
            timeframe,
        )

        async for bar in ws_datasource.fetch():
            if bar:
                await self.dispatch(
                    NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
                )

            if bar and bar.closed:
                logger.info(f"Tick: {symbol}_{timeframe}{strategy}:{bar}")
