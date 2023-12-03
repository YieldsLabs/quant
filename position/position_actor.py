from typing import Union

from core.actors import Actor
from core.events.backtest import BacktestEnded
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
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .position_state_machine import PositionStateMachine
from .position_storage import PositionStorage

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
BrokerPositionEvent = Union[BrokerPositionOpened, BrokerPositionClosed]
ExitSignal = Union[
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    RiskThresholdBreached,
    BacktestEnded,
]

PositionEvent = Union[SignalEvent, ExitSignal, BrokerPositionEvent]


class PositionActor(Actor):
    _EVENTS = [
        GoLongSignalReceived,
        GoShortSignalReceived,
        ExitLongSignalReceived,
        ExitShortSignalReceived,
        BacktestEnded,
        BrokerPositionOpened,
        BrokerPositionClosed,
        RiskThresholdBreached,
    ]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        position_factory: AbstractPositionFactory,
    ):
        super().__init__(symbol, timeframe, strategy)
        self.position_factory = position_factory

        self.sm = PositionStateMachine(self)
        self.state = PositionStorage()

    async def start(self):
        await super().start()

        for event in self._EVENTS:
            self._dispatcher.register(event, self.handle, self._event_filter)

    async def stop(self):
        await super().stop()

        for event in self._EVENTS:
            self._dispatcher.unregister(event, self.handle)

    async def handle(self, event):
        (symbol, timeframe) = self._get_event_key(event)

        if (
            isinstance(event, (GoLongSignalReceived, GoShortSignalReceived))
            and not await self.state.position_exists(symbol, timeframe)
            or not await self._is_event_stale(symbol, timeframe, event)
        ):
            await self.sm.process_event(symbol, event)

    def _event_filter(self, event: PositionEvent) -> bool:
        (symbol, timeframe) = self._get_event_key(event)

        return self._symbol == symbol and self._timeframe == timeframe

    async def _is_event_stale(self, symbol, timeframe, event) -> bool:
        position = await self.state.retrieve_position(symbol, timeframe)

        return position and position.last_modified > event.meta.timestamp

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        position = await self.position_factory.create_position(
            event.signal, event.ohlcv, event.entry_price, event.stop_loss
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
        (symbol, timeframe) = self._get_event_key(event)

        position = await self.state.retrieve_position(symbol, timeframe)

        if position and self.can_close_position(event, position):
            await self.dispatch(PositionCloseRequested(position, event.exit_price))
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

        if isinstance(event, BacktestEnded):
            return True

        return False

    @staticmethod
    def _get_event_key(event: PositionEvent):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal
            if hasattr(event, "position")
            else event
        )

        return (signal.symbol, signal.timeframe)
