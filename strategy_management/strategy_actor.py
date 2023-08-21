import asyncio
import ctypes
from enum import Enum
from typing import Any
from wasmtime import Memory, Store

from core.events.strategy import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.events.ohlcv import NewMarketDataReceived
from core.timeframe import Timeframe

from .abstract_actor import AbstractActor


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0


class StrategyActor(AbstractActor):
    def __init__(self, symbol: str, timeframe: Timeframe, strategy: str, parameters: tuple[int], store: Store, exports: Any):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy = strategy
        self.parameters = parameters
        self.store = store
        self.exports = exports
        self.strategy_id = None

    @property
    def id(self):
        if not self.running:
            raise RuntimeError("Strategy is not started")

        params = self.exports["strategy_parameters"](self.store, self.strategy_id)
        memory = self.exports["memory"]

        return self._get_string_from_memory(self.store, memory, params[0], params[1])

    @property
    def strategy(self):
        return self._strategy

    @property
    def symbol(self):
        return self._symbol

    @property
    def timeframe(self):
        return self._timeframe

    @property
    def running(self):
        return self.strategy_id is not None

    def start(self):
        if self.running:
            raise RuntimeError("Strategy is running")

        self.strategy_id = self.exports[f"register_{self.strategy}"](self.store, *self.parameters)
        self.dispatcher.register(NewMarketDataReceived, self.next)

    def stop(self):
        if not self.running:
            raise RuntimeError("Strategy is not started")

        self.exports[f"unregister_strategy"](self.store, self.strategy_id)
        self.strategy_id = None
        self.dispatcher.unregister(NewMarketDataReceived, self.next)

    async def next(self, event: NewMarketDataReceived):
        if not self.running:
            raise RuntimeError("Strategy is not started")

        data = event.ohlcv
        symbol = event.symbol
        timeframe = event.timeframe

        [action, price] = self.exports["strategy_next"](self.store, self.strategy_id, data.open, data.high, data.low, data.close, data.volume)
        [long_stop_loss, short_stop_loss] = self.exports["strategy_stop_loss"](self.store, self.strategy_id)

        tasks = []

        match action:
            case Action.GO_LONG.value: tasks.append(self.dispatcher.dispatch(
                GoLongSignalReceived(symbol=symbol, strategy=self.id, timeframe=timeframe, entry=price, stop_loss=long_stop_loss)))
            case Action.GO_SHORT.value: tasks.append(self.dispatcher.dispatch(
                GoShortSignalReceived(symbol=symbol, strategy=self.id, timeframe=timeframe, entry=price, stop_loss=short_stop_loss)))
            case Action.EXIT_LONG.value: tasks.append(self.dispatcher.dispatch(
                ExitLongSignalReceived(symbol=symbol, strategy=self.id, timeframe=timeframe, exit=event.ohlcv.close)))
            case Action.EXIT_SHORT.value: tasks.append(self.dispatcher.dispatch(
                ExitShortSignalReceived(symbol=symbol, strategy=self.id, timeframe=timeframe, exit=event.ohlcv.close)))

        await asyncio.gather(*tasks)

    @staticmethod
    def _get_string_from_memory(store: Store, memory: Memory, pointer, length):
        data_ptr = memory.data_ptr(store)
        data_address = ctypes.addressof(data_ptr.contents)
        final_address = data_address + pointer

        if pointer + length > memory.data_len(store):
            raise ValueError("Pointer and length exceed memory bounds")

        byte_array = (ctypes.c_char * length).from_address(final_address)

        return byte_array.value.decode('utf-8')
