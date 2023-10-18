import asyncio
import json
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


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0


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

        data = event.ohlcv

        [action, price] = self.exports["strategy_next"](
            self.store,
            self.register_id,
            data.open,
            data.high,
            data.low,
            data.close,
            data.volume,
        )
        [long_stop_loss, short_stop_loss] = self.exports["strategy_stop_loss"](
            self.store, self.register_id
        )

        action_dispatch_map = {
            Action.GO_LONG.value: lambda: self._dispatch_go_long_signal(
                data, price, long_stop_loss
            ),
            Action.GO_SHORT.value: lambda: self._dispatch_go_short_signal(
                data, price, short_stop_loss
            ),
            Action.EXIT_LONG.value: lambda: self._dispatch_exit_long_signal(
                data, data.close
            ),
            Action.EXIT_SHORT.value: lambda: self._dispatch_exit_short_signal(
                data, data.close
            ),
        }

        dispatch_func = action_dispatch_map.get(action)

        if dispatch_func:
            await dispatch_func()

    def _register_strategy(self):
        (
            signal_parameters,
            filter_parameters,
            stoploss_parameters,
            exit_parameters,
        ) = self._strategy.parameters

        signal_data = json.dumps(signal_parameters).encode()
        filter_data = json.dumps(filter_parameters).encode()
        stoploss_data = json.dumps(stoploss_parameters).encode()
        exit_data = json.dumps(exit_parameters).encode()

        signal_ptr, signal_len = self.allocate_and_write(signal_data)
        filter_ptr, filter_len = self.allocate_and_write(filter_data)
        stoploss_ptr, stoploss_len = self.allocate_and_write(stoploss_data)
        exit_ptr, exit_len = self.allocate_and_write(exit_data)

        self.register_id = self.exports["register"](
            self.store,
            signal_ptr,
            signal_len,
            filter_ptr,
            filter_len,
            stoploss_ptr,
            stoploss_len,
            exit_ptr,
            exit_len,
        )

    def _unregister_strategy(self):
        self.exports["unregister_strategy"](self.store, self.register_id)
        self.register_id = None

    def _filter_events(self, event: NewMarketDataReceived):
        return (
            event.symbol == self._symbol
            and event.timeframe == self._timeframe
            and event.closed is True
        )

    async def _dispatch_go_long_signal(self, data, price, stop_loss):
        await self.dispatch(
            GoLongSignalReceived(
                signal=Signal(
                    self._symbol, self._timeframe, self._strategy, SignalSide.BUY
                ),
                ohlcv=data,
                entry_price=price,
                stop_loss=stop_loss,
            )
        )

    async def _dispatch_go_short_signal(self, data, price, stop_loss):
        await self.dispatch(
            GoShortSignalReceived(
                signal=Signal(
                    self._symbol, self._timeframe, self._strategy, SignalSide.SELL
                ),
                ohlcv=data,
                entry_price=price,
                stop_loss=stop_loss,
            )
        )

    async def _dispatch_exit_long_signal(self, data, exit_price):
        await self.dispatch(
            ExitLongSignalReceived(
                signal=Signal(
                    self._symbol, self._timeframe, self._strategy, SignalSide.BUY
                ),
                ohlcv=data,
                exit_price=exit_price,
            )
        )

    async def _dispatch_exit_short_signal(self, data, exit_price):
        await self.dispatch(
            ExitShortSignalReceived(
                signal=Signal(
                    self._symbol, self._timeframe, self._strategy, SignalSide.SELL
                ),
                ohlcv=data,
                exit_price=exit_price,
            )
        )

    def allocate_and_write(self, data: bytes) -> (int, int):
        ptr = self.exports["allocate"](len(data))
        self.exports["memory"].data[ptr : ptr + len(data)] = data

        return ptr, len(data)
