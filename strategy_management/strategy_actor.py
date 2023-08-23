import asyncio
import ctypes
from enum import Enum
from typing import Any
from core.models.strategy import Strategy
from wasmtime import Memory, Store

from core.events.strategy import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.events.ohlcv import NewMarketDataReceived
from core.models.timeframe import Timeframe
from core.interfaces.abstract_actor import AbstractActor


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0


class StrategyActor(AbstractActor):
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
        self._register_id_lock = asyncio.Lock()

    @property
    def strategy(self):
        return self._strategy

    @property
    def running(self):
        return self.register_id

    async def start(self):
        if self.running:
            raise RuntimeError("Start: strategy is running")

        async with self._register_id_lock:
            self.register_id = self.exports[f"register_{self._strategy_name}"](self.store, *self.parameters)
            self._set_strategy()

        self.dispatcher.register(NewMarketDataReceived, self._strategy_event_filter)

    async def stop(self):
        if not self.running:
            raise RuntimeError("Stop: strategy is not started")

        async with self._register_id_lock:
            self.exports[f"unregister_strategy"](self.store, self.register_id)
            self.register_id = None
    
        self.dispatcher.unregister(NewMarketDataReceived, self._strategy_event_filter)

    async def next(self, event: NewMarketDataReceived):
        if not self.running:
            raise RuntimeError("Next: strategy is not started")
        
        data = event.ohlcv

        [action, price] = self.exports["strategy_next"](self.store, self.register_id, data.open, data.high, data.low, data.close, data.volume)
        [long_stop_loss, short_stop_loss] = self.exports["strategy_stop_loss"](self.store, self.register_id)

        tasks = []

        match action:
            case Action.GO_LONG.value: tasks.append(self.dispatcher.dispatch(
                GoLongSignalReceived(strategy=self.strategy, entry=price, stop_loss=long_stop_loss)))
            case Action.GO_SHORT.value: tasks.append(self.dispatcher.dispatch(
                GoShortSignalReceived(strategy=self.strategy, entry=price, stop_loss=short_stop_loss)))
            case Action.EXIT_LONG.value: tasks.append(self.dispatcher.dispatch(
                ExitLongSignalReceived(strategy=self.strategy, exit=event.ohlcv.close)))
            case Action.EXIT_SHORT.value: tasks.append(self.dispatcher.dispatch(
                ExitShortSignalReceived(strategy=self.strategy, exit=event.ohlcv.close)))

        await asyncio.gather(*tasks)

    async def _strategy_event_filter(self, event: NewMarketDataReceived):
        if event.symbol == self._symbol and event.timeframe == self._timeframe:
            await self.next(event)

    def _set_strategy(self):
        if not self.running:
            raise RuntimeError("ID: strategy is not registered")
        
        params = self.exports["strategy_parameters"](self.store, self.register_id)
        memory = self.exports["memory"]

        strategy_parameters = self._get_string_from_memory(self.store, memory, params[0], params[1])

        self._strategy = Strategy.from_label(f'{self._symbol}_{self._timeframe}{strategy_parameters}')

    @staticmethod
    def _get_string_from_memory(store: Store, memory: Memory, pointer, length):
        data_ptr = memory.data_ptr(store)
        data_address = ctypes.addressof(data_ptr.contents)
        final_address = data_address + pointer

        if pointer + length > memory.data_len(store):
            raise ValueError("Memory: pointer and length exceed memory bounds")

        byte_array = (ctypes.c_char * length).from_address(final_address)

        return byte_array.value.decode('utf-8')
