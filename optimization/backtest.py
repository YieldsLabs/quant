from itertools import product
import random
from typing import List, Type
from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.events.position import PositionReadyToClose
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource


class Backtest(AbstractEventManager):
    def __init__(self, datasource: Type[AbstractDatasource]):
        super().__init__()
        self.datasource = datasource

    async def run(self, symbols: List[str], timeframes: List[Timeframe], lookback: int = 3000):
        symbols_and_timeframes = list(product(symbols, timeframes))

        random.shuffle(symbols_and_timeframes)

        for symbol, timeframe in symbols_and_timeframes:
            historical_data = await self.datasource.fetch(symbol, timeframe, lookback)

            await self._process_historical_data(symbol, timeframe, historical_data)

    async def _process_historical_data(self, symbol: str, timeframe: Timeframe, historical_data):
        last_close = None

        for timestamp, open, high, low, close, volume in historical_data:
            ohlcv = OHLCV(timestamp, float(open), float(high), float(low), float(close), float(volume))

            last_close = float(close)

            await self.dispatcher.dispatch(OHLCVEvent(symbol, timeframe, ohlcv))

        if last_close is not None:
            await self.dispatcher.dispatch(PositionReadyToClose(symbol, timeframe, last_close))
