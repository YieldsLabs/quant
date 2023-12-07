import logging

from core.commands.backtest import BacktestRun
from core.event_decorators import command_handler
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_datasource_factory import AbstractDataSourceFactory
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.models.order import OrderType

logger = logging.getLogger(__name__)


class Backtest(AbstractEventManager):
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
        self.config = config_service.get("backtest")

    @command_handler(BacktestRun)
    async def _backtest_handler(self, command: BacktestRun):
        symbol, timeframe, strategy = (
            command.symbol,
            command.timeframe,
            command.strategy,
        )

        datasource = self.datasource_factory.create(
            command.datasource,
            symbol,
            timeframe,
        )

        actors = [
            self.signal_factory.create_actor(symbol, timeframe, strategy),
            self.position_factory.create_actor(symbol, timeframe, strategy),
            self.risk_factory.create_actor(symbol, timeframe, strategy),
            self.executor_factory.create_actor(
                OrderType.PAPER, symbol, timeframe, strategy
            ),
        ]

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))

        logger.info(
            f"Backtest: strategy={symbol}_{timeframe}{strategy}, lookback={command.in_sample}"
        )

        iterator = datasource.fetch(
            command.in_sample, command.out_sample, self.config["batch_size"]
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

        for actor in actors:
            actor.stop()
