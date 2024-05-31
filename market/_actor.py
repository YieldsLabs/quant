import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Union

from wasmtime import Instance, Linker, Store, WasiConfig

from core.actors import BaseActor
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.mixins import EventHandlerMixin
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.ta import TechAnalysis
from core.models.timeframe import Timeframe
from core.models.timeseries_ref import TimeSeriesRef
from core.models.wasm_type import WasmType
from core.queries.ohlcv import TA, NextBar, PrevBar

MarketEvent = Union[NewMarketDataReceived, NextBar, PrevBar]


class MarketActor(BaseActor, EventHandlerMixin):
    _EVENTS = [NewMarketDataReceived, NextBar, PrevBar, TA]

    def __init__(self, wasm_service: AbstractWasmService):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self._bucket = {}
        self._lock = asyncio.Lock()
        self.wasm_service = wasm_service
        self.store = Store()
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        self.store.set_wasi(wasi_config)
        self.linker = Linker(self.store.engine)
        self.linker.define_wasi()
        self.instance: Optional[Instance] = None

    def on_start(self):
        self.load_instance()

    def load_instance(self):
        module = self.wasm_service.get_module(WasmType.TIMESERIES, self.store.engine)
        self.instance = self.linker.instantiate(self.store, module)

    async def on_receive(self, event: MarketEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(NewMarketDataReceived, self._handle_market)
        self.register_handler(NextBar, self._handle_next_bar)
        self.register_handler(PrevBar, self._handle_prev_bar)
        self.register_handler(TA, self._handle_ta)

    async def _handle_market(self, event: NewMarketDataReceived):
        await self.upsert(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_next_bar(self, event: NextBar) -> OHLCV:
        return await self.next_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_prev_bar(self, event: PrevBar) -> OHLCV:
        return await self.prev_bar(event.symbol, event.timeframe, event.ohlcv)

    async def _handle_ta(self, event: TA) -> TechAnalysis:
        return await self.ta(event.symbol, event.timeframe, event.ohlcv)

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

    async def ta(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        async with self._get_timeseries(symbol, timeframe) as timeseries:
            return timeseries.ta(bar)

    @asynccontextmanager
    async def _get_timeseries(self, symbol: Symbol, timeframe: Timeframe):
        async with self._lock:
            key = (symbol, timeframe)

            if key not in self._bucket:
                exports = self.instance.exports(self.store)
                id = exports["timeseries_register"](self.store)

                self._bucket[key] = TimeSeriesRef(
                    id=id, instance_ref=self.instance, store_ref=self.store
                )

            yield self._bucket[key]
