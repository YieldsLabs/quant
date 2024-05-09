import asyncio

from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.timeseries import Timeseries


class MarketRepository(AbstractMarketRepository):
    def __init__(self, wasm_service: AbstractWasmService):
        super().__init__()
        self._lock = asyncio.Lock()
        self._bucket = {}
        self.wasm_service = wasm_service

    async def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        timeseries = await self._get_timeseries(symbol, timeframe)
        timeseries.add(bar)

    async def find_next_bar(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        timeseries = await self._get_timeseries(symbol, timeframe)

        async for next_bar in timeseries.find_next_bar(bar):
            yield next_bar

    async def _get_timeseries(self, symbol: Symbol, timeframe: Timeframe) -> Timeseries:
        async with self._lock:
            key = (symbol, timeframe)

            if key not in self._bucket:
                self._bucket[key] = Timeseries()

            return self._bucket[key]
