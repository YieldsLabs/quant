import asyncio
import logging
from ctypes import addressof, c_ubyte
from enum import Enum
from typing import Any

from wasmtime import Store

from core.actors.base import BaseActor
from core.events.ohlcv import NewMarketDataReceived
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.models.signal import Signal, SignalSide
from core.models.strategy import Strategy
from core.models.timeframe import Timeframe

logger = logging.getLogger(__name__)


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0
    DO_NOTHING = 0.0

    @classmethod
    def from_raw(cls, value: float):
        for action in cls:
            if action.value == value:
                return action

        raise ValueError(f"No matching Action for float value: {value}")

    def __str__(self):
        return self.name


class SignalActor(BaseActor):
    def __init__(
        self,
        symbol: str,
        timeframe: Timeframe,
        strategy: Strategy,
        store: Store,
        exports: Any,
    ):
        super().__init__(symbol, timeframe, strategy)
        self.store = store
        self.exports = exports
        self.register_id = None
        self._lock = asyncio.Lock()

    async def start(self):
        await super().start()

        async with self._lock:
            self._register_strategy()

        self._dispatcher.register(
            NewMarketDataReceived, self.handle, self._filter_events
        )

    async def stop(self):
        await super().stop()

        async with self._lock:
            self._unregister_strategy()

        self._dispatcher.unregister(NewMarketDataReceived, self.handle)

    async def handle(self, event: NewMarketDataReceived):
        if not await self.running:
            return

        ohlcv = event.ohlcv

        [raw_action, price] = self.exports["strategy_next"](
            self.store,
            self.register_id,
            ohlcv.open,
            ohlcv.high,
            ohlcv.low,
            ohlcv.close,
            ohlcv.volume,
        )

        action = Action.from_raw(raw_action)

        long_stop_loss, short_stop_loss = 0.0, 0.0

        if action in (Action.GO_LONG, Action.GO_SHORT):
            [long_stop_loss, short_stop_loss] = self.exports["strategy_stop_loss"](
                self.store, self.register_id
            )

        logger.debug(
            f"Action: {action} price: {price} stop_loss: lng{long_stop_loss} sht{short_stop_loss}"
        )

        buy_signal = Signal(
            self._symbol, self._timeframe, self._strategy, SignalSide.BUY
        )
        sell_signal = Signal(
            self._symbol, self._timeframe, self._strategy, SignalSide.SELL
        )

        action_event_map = {
            Action.GO_LONG: GoLongSignalReceived(
                signal=buy_signal,
                ohlcv=ohlcv,
                entry_price=price,
                stop_loss=long_stop_loss,
            ),
            Action.GO_SHORT: GoShortSignalReceived(
                signal=sell_signal,
                ohlcv=ohlcv,
                entry_price=price,
                stop_loss=short_stop_loss,
            ),
            Action.EXIT_LONG: ExitLongSignalReceived(
                signal=buy_signal,
                ohlcv=ohlcv,
                exit_price=ohlcv.close,
            ),
            Action.EXIT_SHORT: ExitShortSignalReceived(
                signal=sell_signal,
                ohlcv=ohlcv,
                exit_price=ohlcv.close,
            ),
        }

        event = action_event_map.get(action)

        if event:
            await self.dispatch(event)

    def _register_strategy(self):
        data = {
            "signal": self._strategy.parameters[0],
            "filter": self._strategy.parameters[1],
            "pulse": self._strategy.parameters[2],
            "baseline": self._strategy.parameters[3],
            "stoploss": self._strategy.parameters[4],
            "exit": self._strategy.parameters[5],
        }

        allocation_data = {
            key: self._allocate_and_write(self.store, self.exports, data)
            for key, data in data.items()
        }

        self.register_id = self.exports["register"](
            self.store, *[item for pair in allocation_data.values() for item in pair]
        )

    def _unregister_strategy(self):
        self.exports["unregister_strategy"](self.store, self.register_id)
        self.register_id = None

    def _filter_events(self, event: NewMarketDataReceived):
        return (
            event.symbol == self._symbol
            and event.timeframe == self._timeframe
            and event.closed
        )

    def _allocate_and_write(self, store, exports, data: bytes) -> (int, int):
        ptr = exports["allocate"](store, len(data))
        memory = exports["memory"]

        total_memory_size = memory.data_len(store)
        data_ptr = memory.data_ptr(store)
        data_array = (c_ubyte * total_memory_size).from_address(
            addressof(data_ptr.contents)
        )
        data_array[ptr : ptr + len(data)] = data

        return ptr, len(data)
