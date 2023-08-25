import asyncio
from enum import Enum, auto
from typing import Callable, Tuple, Type, Union
from core.events.backtest import BacktestEnded

from core.events.ohlcv import NewMarketDataReceived
from core.events.order import OrderFilled
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, GoLongSignalReceived, ExitShortSignalReceived, GoShortSignalReceived
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
        PositionState.IDLE: {
            GoLongSignalReceived: (PositionState.WAITING_ORDER, "handle_open_position"),
            GoShortSignalReceived: (PositionState.WAITING_ORDER, "handle_open_position")
        },
        PositionState.WAITING_ORDER: {
            OrderFilled: (PositionState.OPENED, "handle_order_filled"),
            BacktestEnded:(PositionState.CLEANUP, "handle_backtest_end"),
        },
        PositionState.OPENED: {
            ExitLongSignalReceived: (PositionState.IDLE, "handle_exit"),
            ExitShortSignalReceived: (PositionState.IDLE, "handle_exit"),
            RiskThresholdBreached: (PositionState.IDLE, "handle_exit"),
            BacktestEnded:(PositionState.CLEANUP, "handle_backtest_end"),
        },
    }

    def __init__(self, position_manager: Type[AbstractPositionManager]):
        self.state: Tuple[str, PositionState] = ()
        self.position_manager = position_manager
        self.state_lock = asyncio.Lock()

    def get_state(self, symbol: str) -> PositionState:
        for s, state in self.state:
            if s == symbol:
                return state
        return PositionState.IDLE

    def set_state(self, symbol: str, state: PositionState) -> Tuple[str, PositionState]:
        new_state = [(s, state) if s == symbol else (s, st) for s, st in self.state]
        
        if symbol not in [s for s, _ in new_state]:
            new_state.append((symbol, state))
        
        return tuple(new_state)

    async def process_event(self, signal: Signal, event: PortfolioEvent):
        symbol = signal.symbol
        state = self.get_state(symbol)
        next_state, handler_name = self.TRANSITIONS.get(state, {}).get(type(event), (None, None))
        
        if not handler_name:
            return
    
        handler = getattr(self.position_manager, handler_name)

        if not await handler(event):
            return

        async with self.state_lock:
            self.state = self.set_state(symbol, next_state)
