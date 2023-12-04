import logging

from core.commands.backtest import BacktestRun
from core.event_decorators import command_handler
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_backtest import AbstractBacktest
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_datasource_factory import AbstractDataSourceFactory

logger = logging.getLogger(__name__)


class Backtest(AbstractBacktest):
    def __init__(
        self,
        datasource_factory: AbstractDataSourceFactory,
        config_service: AbstractConfig,
    ):
        super().__init__()
        self.datasource_factory = datasource_factory
        self.config = config_service.get("backtest")

    @command_handler(BacktestRun)
    async def _run_backtest(self, command: BacktestRun):
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

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))

        logger.info(
            f"Backtest: strategy={symbol}_{timeframe}{strategy}, lookback={command.in_sample}"
        )

        iterator = datasource.fetch(
            command.in_sample, command.out_sample, self.config["batch_size"]
        )

        async for ohlcv in iterator:
            await self.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv, True))

        last_row = iterator.get_last_row()

        if last_row:
            await self.dispatch(
                BacktestEnded(symbol, timeframe, strategy, last_row.close)
            )
