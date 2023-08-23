from typing import Any, List

from core.event_decorators import event_handler
from core.events.backtest import BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed
from core.models.timeframe import Timeframe
from core.models.ohlcv import OHLCV
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK
from core.interfaces.abstract_backtest import AbstractBacktest


class Backtest(AbstractBacktest):
    def __init__(self):
        super().__init__()

    @event_handler(BacktestStarted)
    async def _on_backtest(self, event: BacktestStarted):
        strategy = event.strategy
        symbol = strategy.symbol
        timeframe = strategy.timeframe

        iterator = event.datasource.fetch(symbol, timeframe, TIMEFRAMES_TO_LOOKBACK[(event.lookback, timeframe)])

        async for data in iterator:
            await self._process_historical_data(symbol, timeframe, data)

        last_row = iterator.get_last_row()

        if last_row:
            last_close = last_row[-2]
            await self.dispatcher.dispatch(PositionClosed(strategy, last_close))

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, data: List[Any]):
        ohlcv = OHLCV.from_list(data)

        await self.dispatcher.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv))
