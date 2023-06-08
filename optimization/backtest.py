from enum import Enum
from itertools import product
import random
from typing import List, Type

from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV, NewMarketDataReceived
from core.events.position import PositionReadyToClose
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource


class Lookback(Enum):
    ONE_MONTH = '1M'
    THREE_MONTH = '3M'


class Backtest(AbstractEventManager):
    TIMEFRAMES_TO_LOOKBACK = {
        (Lookback.ONE_MONTH, Timeframe.ONE_MINUTE): 43200,
        (Lookback.ONE_MONTH, Timeframe.FIVE_MINUTES): 8640,
        (Lookback.ONE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880,

        (Lookback.THREE_MONTH, Timeframe.ONE_MINUTE): 43200 * 3,
        (Lookback.THREE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 3,
        (Lookback.THREE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 3
    }

    def __init__(self, datasource: Type[AbstractDatasource]):
        super().__init__()
        self.datasource = datasource

    async def run(self, symbols: List[str], timeframes: List[Timeframe], lookback: Lookback = Lookback.ONE_MONTH):
        symbols_and_timeframes = list(product(symbols, timeframes))
        random.shuffle(symbols_and_timeframes)

        for symbol, timeframe in symbols_and_timeframes:
            iterator = self.datasource.fetch(symbol, timeframe, self.TIMEFRAMES_TO_LOOKBACK[(lookback, timeframe)])

            async for data in iterator:
                await self._process_historical_data(symbol, timeframe, data)

            last_row = iterator.get_last_row()

            if last_row is not None:
                last_close = last_row[-2]
                await self.dispatcher.dispatch(PositionReadyToClose(symbol, timeframe, last_close))

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, data):
        timestamp, open, high, low, close, volume = data
        ohlcv = OHLCV(timestamp, float(open), float(high), float(low), float(close), float(volume))
        await self.dispatcher.dispatch(NewMarketDataReceived(symbol, timeframe, ohlcv))
