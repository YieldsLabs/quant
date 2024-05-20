import asyncio
from typing import Optional

from wasmtime import Instance, Linker, Store, WasiConfig

from core.event_decorators import event_handler
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.timeseries_ref import TimeSeriesRef
from core.models.wasm_type import WasmType


class MarketRepository(AbstractMarketRepository):
    def __init__(self, wasm_service: AbstractWasmService):
        super().__init__()
        self._lock = asyncio.Lock()
        self._bucket = {}
        self.wasm_service = wasm_service
        self.store = Store()
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        self.store.set_wasi(wasi_config)
        self.linker = Linker(self.store.engine)
        self.linker.define_wasi()
        self.instance: Optional[Instance] = None

        self._load()

    def _load(self):
        module = self.wasm_service.get_module(WasmType.TIMESERIES, self.store.engine)
        self.instance = self.linker.instantiate(self.store, module)

    @event_handler(NewMarketDataReceived)
    async def _market_handler(self, event: NewMarketDataReceived):
        await self.upsert(event.symbol, event.timeframe, event.ohlcv)

    async def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        timeseries = await self._get_timeseries(symbol, timeframe)
        timeseries.add(bar)

    async def find_next_bar(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        timeseries = await self._get_timeseries(symbol, timeframe)
        next_bar = timeseries.find_next_bar(bar)

        while next_bar:
            yield next_bar
            await asyncio.sleep(0.0001)
            next_bar = timeseries.find_next_bar(next_bar)

    async def ta(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        timeseries = await self._get_timeseries(symbol, timeframe)
        ta = timeseries.ta(bar)
        return ta

    async def _get_timeseries(
        self, symbol: Symbol, timeframe: Timeframe
    ) -> TimeSeriesRef:
        async with self._lock:
            key = (symbol, timeframe)

            if key not in self._bucket:
                exports = self.instance.exports(self.store)
                id = exports["timeseries_register"](self.store)

                self._bucket[key] = TimeSeriesRef(
                    id=id, instance_ref=self.instance, store_ref=self.store
                )

            return self._bucket[key]
