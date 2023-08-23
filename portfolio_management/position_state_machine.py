import asyncio
from enum import Enum, auto
from typing import Callable, Tuple, Type, Union

from core.events.ohlcv import NewMarketDataReceived
from core.events.position import OrderFilled, PositionClosed
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, GoLongSignalReceived, ExitShortSignalReceived, GoShortSignalReceived
from core.interfaces.abstract_portfolio_manager import AbstractPortfolioManager


class PositionState(Enum):
    IDLE = auto()
    OPENING = auto()
    OPENED = auto()
    CLOSING = auto()


PortfolioEvent = Union[GoLongSignalReceived, GoShortSignalReceived, ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached, OrderFilled, PositionClosed, NewMarketDataReceived]
HandlerFunction = Callable[[PortfolioEvent], bool]


class PositionStateMachine:
    TRANSITIONS = {
        PositionState.IDLE: {
            GoLongSignalReceived: (PositionState.OPENING, "handle_open_position"),
            GoShortSignalReceived: (PositionState.OPENING, "handle_open_position")
        },
        PositionState.OPENING: {
            OrderFilled: (PositionState.OPENED, "handle_order_filled"),
            PositionClosed: (PositionState.IDLE, "handle_closed_position")
        },
        PositionState.OPENED: {
            ExitLongSignalReceived: (PositionState.CLOSING, "handle_exit"),
            ExitShortSignalReceived: (PositionState.CLOSING, "handle_exit"),
            RiskThresholdBreached: (PositionState.CLOSING, "handle_exit"),
            PositionClosed: (PositionState.IDLE, "handle_closed_position")
        },
        PositionState.CLOSING: {
            PositionClosed: (PositionState.IDLE, "handle_closed_position")
        }
    }

    def __init__(self, portfolio_manager: Type[AbstractPortfolioManager]):
        self.state: Tuple[str, PositionState] = ()
        self.portfolio_manager = portfolio_manager
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

    async def process_event(self, event: PortfolioEvent):
        symbol = event.strategy.symbol
        state = self.get_state(symbol)
        next_state, handler_name = self.TRANSITIONS.get(state, {}).get(type(event), (None, None))
        
        if not handler_name:
            return
    
        handler = getattr(self.portfolio_manager, handler_name)

        if not await handler(event):
            return

        async with self.state_lock:
            self.state = self.set_state(symbol, next_state)
