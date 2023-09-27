import asyncio
from typing import Union

from core.commands.account import UpdateAccountSize
from core.event_decorators import command_handler
from core.events.account import PositionAccountUpdated
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.portfolio import GetTotalPnL

from .position_state_machine import PositionStateMachine
from .position_storage import PositionStorage

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
PositionEvent = Union[BrokerPositionOpened, BrokerPositionClosed]
ExitSignal = Union[
    ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached
]


class PositionActor(AbstractActor):
    SIGNAL_EVENTS = (GoLongSignalReceived, GoShortSignalReceived)
    EXIT_EVENTS = (ExitLongSignalReceived, ExitShortSignalReceived)
    POSITION_EVENTS = (
        BrokerPositionOpened,
        BrokerPositionClosed,
        RiskThresholdBreached,
    )

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        position_factory: AbstractPositionFactory,
        initial_account_size: int,
    ):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy = strategy

        self.account_size = initial_account_size
        self.position_factory = position_factory

        self._lock = asyncio.Lock()
        self._running = False

        self.sm = PositionStateMachine(self)
        self.state = PositionStorage()

    @property
    def id(self):
        return f"{self._symbol}_{self._timeframe}"

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
    async def running(self):
        async with self._lock:
            return self._running

    async def start(self):
        if await self.running:
            raise RuntimeError("Start: position is running")

        for event in self.SIGNAL_EVENTS + self.EXIT_EVENTS + self.POSITION_EVENTS:
            self._dispatcher.register(event, self.handle, self._event_filter)

        async with self._lock:
            self._running = True

    async def stop(self):
        if not await self.running:
            raise RuntimeError("Stop: position is not started")

        for event in self.SIGNAL_EVENTS + self.EXIT_EVENTS + self.POSITION_EVENTS:
            self._dispatcher.unregister(event, self.handle)

        async with self._lock:
            self._running = False

    async def handle(self, event):
        signal = (
            event.signal
            if isinstance(event, self.SIGNAL_EVENTS + self.EXIT_EVENTS)
            else event.position.signal
        )

        if (
            isinstance(event, self.SIGNAL_EVENTS)
            and not await self.state.position_exists(signal)
        ) or not await self._is_event_stale(signal, event):
            await self.sm.process_event(signal, event)

    def _event_filter(
        self, event: Union[SignalEvent, ExitSignal, PositionEvent]
    ) -> bool:
        signal = event.signal if hasattr(event, "signal") else event.position.signal

        return self._symbol == signal.symbol and self._timeframe == signal.timeframe

    async def _is_event_stale(self, signal, event) -> bool:
        position = await self.state.retrieve_position(signal)

        return position and position.last_modified > event.meta.timestamp

    @command_handler(UpdateAccountSize)
    async def update_account_size(self, command: UpdateAccountSize):
        self.account_size = command.amount

        await self.dispatch(PositionAccountUpdated(self.account_size))

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        account_size = self.account_size + await self.query(GetTotalPnL(event.signal))

        position = self.position_factory.create_position(
            event.signal, event.ohlcv, account_size, event.entry_price, event.stop_loss
        )

        await self.state.store_position(position)

        await self.dispatch(PositionInitialized(position))

        return True

    async def handle_position_opened(self, event: BrokerPositionOpened) -> bool:
        await self.state.update_stored_position(event.position)

        await self.dispatch(PositionOpened(event.position))

        return True

    async def handle_position_closed(self, event: BrokerPositionClosed) -> bool:
        await self.state.close_stored_position(event.position)

        await self.dispatch(PositionClosed(event.position))

        return True

    async def handle_exit_received(self, event: ExitSignal) -> bool:
        if isinstance(event, ExitLongSignalReceived) or isinstance(
            event, ExitShortSignalReceived
        ):
            signal = event.signal
        else:
            signal = event.position.signal

        position = await self.state.retrieve_position(signal)

        if position and self.can_close_position(event, position):
            position = position.close(event.ohlcv.timestamp).update_prices(
                event.exit_price
            )

            await self.dispatch(PositionCloseRequested(position))

            return True

        return False

    @staticmethod
    def can_close_position(event, position: Position) -> bool:
        if position.side == PositionSide.LONG and isinstance(
            event, ExitLongSignalReceived
        ):
            return position.entry_price < event.exit_price

        if position.side == PositionSide.SHORT and isinstance(
            event, ExitShortSignalReceived
        ):
            return position.entry_price > event.exit_price

        if (
            isinstance(event, RiskThresholdBreached)
            and position.side == event.position.side
        ):
            return True

        return False
