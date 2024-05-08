import asyncio

from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.timeseries import Timeseries


class MarketRepository(AbstractMarketRepository):
    def __init__(self):
        super().__init__()
        self._lock = asyncio.Lock()
        self._store = {}

    async def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        store = await self._get_store(symbol, timeframe)
        store.enqueue(bar)

    async def find_next_bar(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        store = await self._get_store(symbol, timeframe)

        async for next_bar in store.find_next_bar(bar):
            yield next_bar

    async def _get_store(self, symbol: Symbol, timeframe: Timeframe):
        async with self._lock:
            key = (symbol, timeframe)

            if key not in self._store:
                self._store[key] = Timeseries()

            return self._store[key]
