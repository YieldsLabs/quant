import logging
from typing import Any, List

from core.commands.backtest import BacktestRun
from core.event_decorators import command_handler
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.models.timeframe import Timeframe
from core.models.ohlcv import OHLCV
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK
from core.interfaces.abstract_backtest import AbstractBacktest


logger = logging.getLogger(__name__)


class Backtest(AbstractBacktest):
    def __init__(self):
        super().__init__()

    @command_handler(BacktestRun)
    async def _run_backtest(self, command: BacktestRun):
        datasource = command.datasource
        symbol = command.symbol
        timeframe = command.timeframe
        lookback = command.lookback
        batch_size = command.batch_size

        logger.info(f"Backtest: symbol={symbol}, timeframe={timeframe}")

        iterator = datasource.fetch(symbol, timeframe, TIMEFRAMES_TO_LOOKBACK[(lookback, timeframe)], batch_size)

        await self.dispatch(BacktestStarted(symbol, timeframe))

        async for data in iterator:
            await self._process_historical_data(symbol, timeframe, data)

        last_row = iterator.get_last_row()

        if last_row:
            last_close = last_row[-2]
            await self.dispatch(BacktestEnded(symbol, timeframe, last_close))

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, data: List[Any]):
        ohlcv = OHLCV.from_list(data)

        await self.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv))
