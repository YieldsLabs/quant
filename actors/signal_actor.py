import asyncio
import ctypes
from enum import Enum
from functools import lru_cache
from typing import Any
from wasmtime import Memory, Store

from core.models.signal import Signal, SignalSide
from core.models.strategy import Strategy
from core.events.signal import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.events.ohlcv import NewMarketDataReceived
from core.models.timeframe import Timeframe
from core.interfaces.abstract_actor import AbstractActor


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0


class SignalActor(AbstractActor):
    def __init__(self, symbol: str, timeframe: Timeframe, strategy_name: str, parameters: tuple[int], store: Store, exports: Any):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy_name = strategy_name
        self._strategy = None

        self.parameters = parameters
        self.store = store
        self.exports = exports
        self.register_id = None
        self._lock = asyncio.Lock()

    @property
    def id(self):
        if not self._strategy:
            raise RuntimeError("Id: Strategy is not started")
        
        return str(self._strategy)

    @property
    def running(self):
        return bool(self.register_id)

    async def start(self):
        if await self.running:
            raise RuntimeError("Start: strategy is running")

        async with self._lock:
            self._register_strategy()
            self._set_strategy()

        self.dispatcher.register(NewMarketDataReceived, self._signal_event_filter)

    async def stop(self):
        if not await self.running:
            raise RuntimeError("Stop: strategy is not started")

        async with self._lock:
            self._unregister_strategy()
    
        self.dispatcher.unregister(NewMarketDataReceived, self._signal_event_filter)

    async def next(self, event: NewMarketDataReceived):
        if not await self.running:
            return
    
        data = event.ohlcv

        [action, price] = self.exports["strategy_next"](self.store, self.register_id, data.open, data.high, data.low, data.close, data.volume)
        [long_stop_loss, short_stop_loss] = self.exports["strategy_stop_loss"](self.store, self.register_id)

        action_dispatch_map = {
            Action.GO_LONG.value: lambda: self._dispatch_go_long_signal(data, price, long_stop_loss),
            Action.GO_SHORT.value: lambda: self._dispatch_go_short_signal(data, price, short_stop_loss),
            Action.EXIT_LONG.value: lambda: self._dispatch_exit_long_signal(data, data.close),
            Action.EXIT_SHORT.value: lambda: self._dispatch_exit_short_signal(data, data.close)
        }

        dispatch_func = action_dispatch_map.get(action)
        
        if dispatch_func:
            await dispatch_func()

    def _register_strategy(self):
        self.register_id = self.exports[f"register_{self._strategy_name}"](self.store, *self.parameters)

    def _unregister_strategy(self):
        self.exports["unregister_strategy"](self.store, self.register_id)
        self.register_id = None
    
    async def _signal_event_filter(self, event: NewMarketDataReceived):
        if event.symbol == self._symbol and event.timeframe == self._timeframe:
            await self.next(event)

    def _set_strategy(self):
        params = self.exports["strategy_parameters"](self.store, self.register_id)
        memory = self.exports["memory"]

        strategy_parameters = self._get_string_from_memory(self.store, memory, params[0], params[1])
        self._strategy = Strategy.from_label(strategy_parameters)

    async def _dispatch_go_long_signal(self, data, price, stop_loss):
        await self.dispatcher.dispatch(
            GoLongSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.BUY), ohlcv=data, entry_price=price, stop_loss=stop_loss))

    async def _dispatch_go_short_signal(self, data, price, stop_loss):
        await self.dispatcher.dispatch(
            GoShortSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.SELL), ohlcv=data, entry_price=price, stop_loss=stop_loss))

    async def _dispatch_exit_long_signal(self, data, exit_price):
        await self.dispatcher.dispatch(
            ExitLongSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.BUY), ohlcv=data, exit_price=exit_price))

    async def _dispatch_exit_short_signal(self, data, exit_price):
        await self.dispatcher.dispatch(
            ExitShortSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.SELL), ohlcv=data, exit_price=exit_price))

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_string_from_memory(store: Store, memory: Memory, pointer, length):
        data_ptr = memory.data_ptr(store)
        data_address = ctypes.addressof(data_ptr.contents)
        final_address = data_address + pointer

        if pointer + length > memory.data_len(store):
            raise ValueError("Memory: pointer and length exceed memory bounds")

        byte_array = (ctypes.c_char * length).from_address(final_address)

        return byte_array.value.decode('utf-8')
