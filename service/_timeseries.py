import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.interfaces.abstract_wasm_manager import AbstractWasmManager
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.timeseries_ref import TimeSeriesRef
from core.models.wasm_type import WasmType


class TimeSeriesService(AbstractTimeSeriesService):
    def __init__(self, wasm_manager: AbstractWasmManager):
        self._bucket = {}
        self._lock = asyncio.Lock()
        self._wasm_manager = wasm_manager
        self._wasm = WasmType.TIMESERIES

    async def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            timeseries.add(bar)

    async def next_bar(
        self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV
    ) -> Optional[OHLCV]:
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            return timeseries.next_bar(bar)

    async def prev_bar(
        self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV
    ) -> Optional[OHLCV]:
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            return timeseries.prev_bar(bar)

    async def back_n_bars(
        self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV, n: int
    ) -> Optional[OHLCV]:
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            return timeseries.back_n_bars(bar, n)

    async def ta(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            return timeseries.ta(bar)

    @asynccontextmanager
    async def _get_timeseries(self, symbol: Symbol, timeframe: Timeframe):
        async with self._lock:
            key = (symbol, timeframe)
            if key not in self._bucket:
                instance, store = self._wasm_manager.get_instance(self._wasm)
                exports = instance.exports(store)
                id = exports["timeseries_register"](store)
                self._bucket[key] = TimeSeriesRef(
                    id=id, instance_ref=instance, store_ref=store
                )
            yield self._bucket[key]
