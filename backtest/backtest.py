import logging
from typing import Any, List

from core.commands.backtest import BacktestRun
from core.event_decorators import command_handler
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_backtest import AbstractBacktest
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

logger = logging.getLogger(__name__)


class Backtest(AbstractBacktest):
    def __init__(self, batch_size: int):
        super().__init__()
        self.batch_size = batch_size

    @command_handler(BacktestRun)
    async def _run_backtest(self, command: BacktestRun):
        datasource = command.datasource
        symbol = command.symbol
        timeframe = command.timeframe
        strategy = command.strategy
        in_sample = command.in_sample
        out_sample = command.out_sample

        logger.info(
            f"Backtest: strategy={symbol}_{timeframe}{strategy}, lookback={in_sample}"
        )

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))
        iterator = datasource.fetch(
            symbol, timeframe, in_sample, out_sample, self.batch_size
        )

        async for data in iterator:
            await self._process_historical_data(symbol, timeframe, data)

        last_row = iterator.get_last_row()

        if last_row:
            last_close = last_row[-2]
            await self.dispatch(BacktestEnded(symbol, timeframe, strategy, last_close))

    async def _process_historical_data(
        self, symbol: Symbol, timeframe: Timeframe, data: List[Any]
    ):
        ohlcv = OHLCV.from_list(data)
        await self.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv, True))
