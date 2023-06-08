import asyncio
from enum import Enum, auto
from typing import Callable, Dict, Type, Union

from core.events.ohlcv import NewMarketDataReceived
from core.events.position import OrderFilled, PositionClosed
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, GoLongSignalReceived, ExitShortSignalReceived, GoShortSignalReceived

from .abstract_portfolio_manager import AbstractPortfolioManager


class PositionState(Enum):
    IDLE = auto()
    OPENING = auto()
    OPENED = auto()
    CLOSING = auto()


PortfolioEvent = Union[GoLongSignalReceived, GoShortSignalReceived, ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached, OrderFilled, PositionClosed, NewMarketDataReceived]
HandlerFunction = Callable[[PortfolioEvent], bool]


class PositionStateMachine:
    def __init__(self, portfolio_manager: Type[AbstractPortfolioManager]):
        self.state: Dict[str, PositionState] = {}
        self.state_lock = asyncio.Lock()

        transitions = {
            PositionState.IDLE: {
                GoLongSignalReceived: (PositionState.OPENING, portfolio_manager.handle_open_position),
                GoShortSignalReceived: (PositionState.OPENING, portfolio_manager.handle_open_position)
            },
            PositionState.OPENING: {
                OrderFilled: (PositionState.OPENED, portfolio_manager.handle_order_filled)
            },
            PositionState.OPENED: {
                NewMarketDataReceived: (PositionState.OPENED, portfolio_manager.handle_market),
                ExitLongSignalReceived: (PositionState.CLOSING, portfolio_manager.handle_exit),
                ExitShortSignalReceived: (PositionState.CLOSING, portfolio_manager.handle_exit),
                RiskThresholdBreached: (PositionState.CLOSING, portfolio_manager.handle_exit)
            },
            PositionState.CLOSING: {
                PositionClosed: (PositionState.IDLE, portfolio_manager.handle_closed_position)
            }
        }

        self._state_handlers: Dict[(PositionState, Type[PortfolioEvent]), HandlerFunction] = {}

        for state, event_dict in transitions.items():
            for event, (next_state, handler) in event_dict.items():
                self._state_handlers[(state, event)] = (next_state, handler)

    def get_state(self, symbol: str) -> PositionState:
        return self.state.get(symbol, PositionState.IDLE)

    async def set_state(self, symbol: str, state: PositionState):
        async with self.state_lock:
            self.state[symbol] = state

    async def process_event(self, event: PortfolioEvent):
        symbol = event.symbol
        state = self.get_state(symbol)

        next_state, handler = self._state_handlers.get((state, type(event)), (state, None))

        if handler is None or not await handler(event):
            return

        await self.set_state(symbol, next_state)
