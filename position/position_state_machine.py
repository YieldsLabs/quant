import asyncio
from enum import Enum, auto
from typing import Callable, Dict, Type, Union
from core.events.backtest import BacktestEnded

from core.events.ohlcv import NewMarketDataReceived
from core.events.order import OrderFilled
from core.events.risk import RiskThresholdBreached
from core.events.signal import ExitLongSignalReceived, GoLongSignalReceived, ExitShortSignalReceived, GoShortSignalReceived
from core.interfaces.abstract_position_manager import AbstractPositionManager
from core.models.signal import Signal


class PositionState(Enum):
    IDLE = auto()
    WAITING_ORDER = auto()
    OPENED = auto()
    CLEANUP = auto()


PortfolioEvent = Union[GoLongSignalReceived, GoShortSignalReceived, ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached, OrderFilled, NewMarketDataReceived, BacktestEnded]
HandlerFunction = Callable[[PortfolioEvent], bool]


class PositionStateMachine:
    TRANSITIONS = {
        (PositionState.IDLE, GoLongSignalReceived): (PositionState.WAITING_ORDER, "handle_open_position"),
        (PositionState.IDLE, GoShortSignalReceived): (PositionState.WAITING_ORDER, "handle_open_position"),
        (PositionState.WAITING_ORDER, OrderFilled): (PositionState.OPENED, "handle_order_filled"),
        (PositionState.WAITING_ORDER, BacktestEnded): (PositionState.CLEANUP, "handle_backtest_end"),
        (PositionState.OPENED, ExitLongSignalReceived): (PositionState.IDLE, "handle_exit"),
        (PositionState.OPENED, ExitShortSignalReceived): (PositionState.IDLE, "handle_exit"),
        (PositionState.OPENED, RiskThresholdBreached): (PositionState.IDLE, "handle_exit"),
        (PositionState.OPENED, BacktestEnded): (PositionState.CLEANUP, "handle_backtest_end"),
    }

    def __init__(self, position_manager: Type[AbstractPositionManager]):
        self._state: Dict[str, PositionState] = {}
        self._position_manager = position_manager
        self._state_lock = asyncio.Lock()

    async def _get_state(self, symbol: str) -> PositionState:
        async with self._state_lock:
            return self._state.get(symbol, PositionState.IDLE)

    async def _set_state(self, symbol: str, state: PositionState) -> None:
        async with self._state_lock:
            self._state[symbol] = state

    async def process_event(self, signal: Signal, event: PortfolioEvent):
        symbol = signal.symbol
        current_state = await self._get_state(symbol)
        
        if not self._is_valid_state(current_state, event):
            raise ValueError(f"Cannot process event for symbol {symbol} in state {current_state}")

        next_state, handler_name = self.TRANSITIONS[(current_state, type(event))]
        
        handler = getattr(self._position_manager, handler_name)

        if not await handler(event):
            return

        await self._set_state(symbol, next_state)

    def _is_valid_state(self, state: PositionState, event: PortfolioEvent) -> bool:
        return (state, type(event)) in self.TRANSITIONS