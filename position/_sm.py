import asyncio
import logging
from enum import Enum, auto
from typing import Callable, Dict, Tuple, Type, Union

from core.events.backtest import BacktestEnded
from core.events.position import (
    BrokerPositionAdjusted,
    BrokerPositionClosed,
    BrokerPositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
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


PositionEvent = Union[
    BrokerPositionOpened,
    BrokerPositionAdjusted,
    BrokerPositionClosed,
    GoLongSignalReceived,
    GoShortSignalReceived,
    RiskThresholdBreached,
    BacktestEnded,
]

HandlerFunction = Callable[[PositionEvent], bool]
Transitions = Dict[Tuple[PositionState, PositionEvent], Tuple[PositionState, str]]

LONG_TRANSITIONS: Transitions = {
    (PositionState.IDLE, GoLongSignalReceived): (
        PositionState.WAITING_BROKER_CONFIRMATION,
        "handle_signal_received",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BrokerPositionOpened): (
        PositionState.OPENED,
        "handle_position_opened",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BrokerPositionClosed): (
        PositionState.IDLE,
        "handle_position_closed",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BacktestEnded): (
        PositionState.CLOSE,
        "handle_backtest",
    ),
    (PositionState.OPENED, BrokerPositionAdjusted): (
        PositionState.OPENED,
        "handle_position_adjusted",
    ),
    (PositionState.OPENED, RiskThresholdBreached): (
        PositionState.CLOSE,
        "handle_exit_received",
    ),
    (PositionState.OPENED, BacktestEnded): (
        PositionState.CLOSE,
        "handle_backtest",
    ),
    (PositionState.CLOSE, BrokerPositionClosed): (
        PositionState.IDLE,
        "handle_position_closed",
    ),
}

SHORT_TRANSITIONS: Transitions = {
    (PositionState.IDLE, GoShortSignalReceived): (
        PositionState.WAITING_BROKER_CONFIRMATION,
        "handle_signal_received",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BrokerPositionOpened): (
        PositionState.OPENED,
        "handle_position_opened",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BrokerPositionClosed): (
        PositionState.IDLE,
        "handle_position_closed",
    ),
    (PositionState.WAITING_BROKER_CONFIRMATION, BacktestEnded): (
        PositionState.CLOSE,
        "handle_backtest",
    ),
    (PositionState.OPENED, BrokerPositionAdjusted): (
        PositionState.OPENED,
        "handle_position_adjusted",
    ),
    (PositionState.OPENED, RiskThresholdBreached): (
        PositionState.CLOSE,
        "handle_exit_received",
    ),
    (PositionState.OPENED, BacktestEnded): (
        PositionState.CLOSE,
        "handle_backtest",
    ),
    (PositionState.CLOSE, BrokerPositionClosed): (
        PositionState.IDLE,
        "handle_position_closed",
    ),
}


class PositionStateMachine:
    def __init__(
        self, position_manager: Type[AbstractPositionManager], transitions: Transitions
    ):
        self._state: Dict[str, PositionState] = {}
        self._position_manager = position_manager
        self._transitions = transitions
        self._lock = asyncio.Lock()

    async def _get_state(self, symbol: Symbol) -> PositionState:
        async with self._lock:
            return self._state.get(symbol, PositionState.IDLE)

    async def _set_state(self, symbol: Symbol, state: PositionState) -> None:
        async with self._lock:
            self._state[symbol] = state

    async def process_event(self, symbol: Symbol, event: PositionEvent):
        current_state = await self._get_state(symbol)

        if not self._is_valid_state(self._transitions, current_state, event):
            return

        next_state, handler_name = self._transitions[(current_state, type(event))]

        handler = getattr(self._position_manager, handler_name)

        if not await handler(event):
            return

        await self._set_state(symbol, next_state)

        logger.debug(
            f"SM: symbol={symbol}, event={event}, curr_state={current_state}, next_state={next_state}"
        )

    @staticmethod
    def _is_valid_state(
        transitions: Transitions, state: PositionState, event: PositionEvent
    ) -> bool:
        return (state, type(event)) in transitions
