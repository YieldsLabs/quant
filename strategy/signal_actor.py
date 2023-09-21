import asyncio
from enum import Enum
from typing import Any
from wasmtime import Store

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
    def __init__(self, symbol: str, timeframe: Timeframe, strategy: Strategy, store: Store, exports: Any):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy = strategy

        self.store = store
        self.exports = exports
        self.register_id = None
        self._lock = asyncio.Lock()

    @property
    def id(self):
        if not self._strategy:
            raise RuntimeError("Id: Strategy is not started")
        
        return f"{self._symbol}_{self._timeframe}{self._strategy}"
    
    @property
    def symbol(self):
        return self._symbol
    
    @property
    def timeframe(self):
        return self._timeframe
    
    @property
    def strategy(self):
        return self._strategy

    @property
    def running(self):
        return bool(self.register_id)

    async def start(self):
        if self.running:
            raise RuntimeError("Start: strategy is running")

        async with self._lock:
            self._register_strategy()

        self._dispatcher.register(NewMarketDataReceived, self.handle, self._filter_events)

    async def stop(self):
        if not self.running:
            raise RuntimeError("Stop: strategy is not started")

        async with self._lock:
            self._unregister_strategy()
    
        self._dispatcher.unregister(NewMarketDataReceived, self.handle)

    async def handle(self, event: NewMarketDataReceived):
        if not self.running:
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
        (signal_parameters, filter_parameters, stoploss_parameters) = self._strategy.parameters
        strategy_parameters = signal_parameters + filter_parameters + stoploss_parameters

        self.register_id = self.exports[f"register_{self._strategy.name}"](self.store, *strategy_parameters)

    def _unregister_strategy(self):
        self.exports["unregister_strategy"](self.store, self.register_id)
        self.register_id = None
    
    def _filter_events(self, event: NewMarketDataReceived):
        return event.symbol == self._symbol and event.timeframe == self._timeframe and event.closed == True

    async def _dispatch_go_long_signal(self, data, price, stop_loss):
        await self.dispatch(
            GoLongSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.BUY), ohlcv=data, entry_price=price, stop_loss=stop_loss))

    async def _dispatch_go_short_signal(self, data, price, stop_loss):
        await self.dispatch(
            GoShortSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.SELL), ohlcv=data, entry_price=price, stop_loss=stop_loss))

    async def _dispatch_exit_long_signal(self, data, exit_price):
        await self.dispatch(
            ExitLongSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.BUY), ohlcv=data, exit_price=exit_price))

    async def _dispatch_exit_short_signal(self, data, exit_price):
        await self.dispatch(
            ExitShortSignalReceived(signal=Signal(self._symbol, self._timeframe, self._strategy, SignalSide.SELL), ohlcv=data, exit_price=exit_price))
