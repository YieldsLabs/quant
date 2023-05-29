import asyncio
from enum import Enum, auto
from typing import Dict, Type, Union
from core.events.ohlcv import OHLCVEvent
from core.events.position import OrderFilled, PositionClosed
from core.events.risk import RiskExit

from core.events.strategy import LongExit, LongGo, ShortExit, ShortGo
from .abstract_portfolio_manager import AbstractPortfolioManager


class PositionState(Enum):
    IDLE = auto()
    OPENING = auto()
    OPENED = auto()
    CLOSING = auto()


PortfolioEvent = Union[LongGo, ShortGo, LongExit, ShortExit, RiskExit, OrderFilled, PositionClosed, OHLCVEvent]


class PositionStateMachine:
    def __init__(self, portfolio_manager: Type[AbstractPortfolioManager]):
        self.state: Dict[str, PositionState] = {}
        self.state_lock = asyncio.Lock()
        self._state_handlers = {
            (PositionState.IDLE, LongGo): portfolio_manager.handle_open_position,
            (PositionState.IDLE, ShortGo): portfolio_manager.handle_open_position,
            (PositionState.OPENING, OrderFilled): portfolio_manager.handle_order_filled,
            (PositionState.OPENED, OHLCVEvent): portfolio_manager.handle_market,
            (PositionState.OPENED, LongExit): portfolio_manager.handle_exit,
            (PositionState.OPENED, ShortExit): portfolio_manager.handle_exit,
            (PositionState.OPENED, RiskExit): portfolio_manager.handle_exit,
            (PositionState.CLOSING, PositionClosed): portfolio_manager.handle_closed_position,
        }

    def next_state(self, state: PositionState, event: PortfolioEvent) -> PositionState:
        next_state_mapping = {
            PositionState.IDLE: {
                LongGo: PositionState.OPENING,
                ShortGo: PositionState.OPENING
            },
            PositionState.OPENING: {
                OrderFilled: PositionState.OPENED
            },
            PositionState.OPENED: {
                LongExit: PositionState.CLOSING,
                ShortExit: PositionState.CLOSING,
                RiskExit: PositionState.CLOSING,
                OHLCVEvent: PositionState.OPENED
            },
            PositionState.CLOSING: {
                PositionClosed: PositionState.IDLE
            }
        }

        return next_state_mapping[state].get(type(event), state)

    async def process_event(self, event: PortfolioEvent):
        symbol = event.symbol

        async with self.state_lock:
            state = self.state.get(symbol, PositionState.IDLE)

        handler = self._state_handlers.get((state, type(event)))

        if handler is None or not await handler(event):
            return

        async with self.state_lock:
            self.state[symbol] = self.next_state(state, event)
