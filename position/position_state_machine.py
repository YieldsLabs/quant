import asyncio
import logging
from enum import Enum, auto
from typing import Callable, Dict, Type, Union

from core.events.backtest import BacktestEnded
from core.events.position import BrokerPositionClosed, BrokerPositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_position_manager import AbstractPositionManager
from core.models.symbol import Symbol

logger = logging.getLogger(__name__)


class PositionState(Enum):
    IDLE = auto()
    WAITING_BROKER_CONFIRMATION = auto()
    OPENED = auto()
    CLOSE = auto()


PortfolioEvent = Union[
    BrokerPositionOpened,
    BrokerPositionClosed,
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    RiskThresholdBreached,
]

HandlerFunction = Callable[[PortfolioEvent], bool]


class PositionStateMachine:
    TRANSITIONS = {
        (PositionState.IDLE, GoLongSignalReceived): (
            PositionState.WAITING_BROKER_CONFIRMATION,
            "handle_signal_received",
        ),
        (PositionState.IDLE, GoShortSignalReceived): (
            PositionState.WAITING_BROKER_CONFIRMATION,
            "handle_signal_received",
        ),
        (PositionState.WAITING_BROKER_CONFIRMATION, BrokerPositionOpened): (
            PositionState.OPENED,
            "handle_position_opened",
        ),
        (PositionState.WAITING_BROKER_CONFIRMATION, BacktestEnded): (
            PositionState.CLOSE,
            "handle_exit_received",
        ),
        (PositionState.OPENED, ExitLongSignalReceived): (
            PositionState.CLOSE,
            "handle_exit_received",
        ),
        (PositionState.OPENED, ExitShortSignalReceived): (
            PositionState.CLOSE,
            "handle_exit_received",
        ),
        (PositionState.OPENED, RiskThresholdBreached): (
            PositionState.CLOSE,
            "handle_exit_received",
        ),
        (PositionState.OPENED, BacktestEnded): (
            PositionState.CLOSE,
            "handle_exit_received",
        ),
        (PositionState.CLOSE, BrokerPositionClosed): (
            PositionState.IDLE,
            "handle_position_closed",
        ),
    }

    def __init__(self, position_manager: Type[AbstractPositionManager]):
        self._state: Dict[str, PositionState] = {}
        self._position_manager = position_manager
        self._state_lock = asyncio.Lock()

    async def _get_state(self, symbol: Symbol) -> PositionState:
        async with self._state_lock:
            return self._state.get(symbol, PositionState.IDLE)

    async def _set_state(self, symbol: Symbol, state: PositionState) -> None:
        async with self._state_lock:
            self._state[symbol] = state

    async def process_event(self, symbol: Symbol, event: PortfolioEvent):
        current_state = await self._get_state(symbol)

        if not self._is_valid_state(current_state, event):
            return

        next_state, handler_name = self.TRANSITIONS[(current_state, type(event))]

        handler = getattr(self._position_manager, handler_name)

        if not await handler(event):
            return

        await self._set_state(symbol, next_state)

        logger.debug(f"Position: symbol={symbol}, state={next_state}")

    def _is_valid_state(self, state: PositionState, event: PortfolioEvent) -> bool:
        return (state, type(event)) in self.TRANSITIONS
