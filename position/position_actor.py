import asyncio
from typing import Union


from core.events.position import PositionCloseRequested, PositionClosed, PositionInitialized, PositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.signal import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position, PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .position_storage import PositionStorage
from .position_state_machine import PositionStateMachine

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
PositionEvent = Union[PositionOpened, PositionClosed]
ExitSignal = Union[ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached]

class PositionActor(AbstractActor):
    SIGNAL_EVENTS = (GoLongSignalReceived, GoShortSignalReceived)
    EXIT_EVENTS = (ExitLongSignalReceived, ExitShortSignalReceived)
    POSITION_EVENTS = (PositionOpened, PositionClosed, RiskThresholdBreached)

    def __init__(self, symbol: Symbol, timeframe: Timeframe, position_factory: AbstractPositionFactory, initial_account_size: int):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe

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
    async def running(self):
        async with self._lock:
            return self._running 
    
    async def start(self):
        if await self.running:
            raise RuntimeError("Start: risk is running")

        async with self._lock:
            self._running = True

        for event in self.SIGNAL_EVENTS + self.EXIT_EVENTS + self.POSITION_EVENTS:
            self.dispatcher.register(event, self._event_filter)


    async def stop(self):
        if not await self.running:
            raise RuntimeError("Stop: risk is not started")
        
        async with self._lock:
            self._running = False

        for event in self.SIGNAL_EVENTS + self.EXIT_EVENTS + self.POSITION_EVENTS:
            self.dispatcher.unregister(event, self._event_filter)

    async def handle(self, event):
        if isinstance(event, self.SIGNAL_EVENTS + self.EXIT_EVENTS):
            signal = event.signal
        else:
            signal = event.position.signal

        await self.sm.process_event(signal, event)

    async def _event_filter(self, event: Union[SignalEvent, ExitSignal, PositionEvent]):
        if isinstance(event, self.SIGNAL_EVENTS + self.EXIT_EVENTS):
            signal = event.signal
        else:
            signal = event.position.signal

        if self._symbol == signal.symbol and self._timeframe == signal.timeframe:
            if isinstance(event, (self.SIGNAL_EVENTS)):
                if not await self.state.position_exists(signal):
                    await self.handle(event)
            elif not await self._is_event_stale(signal, event):
                await self.handle(event)

    async def _is_event_stale(self, signal, event) -> bool:
        position = await self.state.retrieve_position(signal)
        
        return position and position.last_modified > event.meta.timestamp

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        account_size = self.account_size

        position = self.position_factory.create_position(
            event.signal,
            account_size,
            event.entry_price,
            event.stop_loss
        )

        await self.state.store_position(position)

        await self.dispatcher.dispatch(PositionInitialized(position))

        return True

    async def handle_position_opened(self, event: PositionOpened) -> bool:
        await self.state.update_stored_position(event.position)
        
        return True
    
    async def handle_position_closed(self, event: PositionClosed) -> bool:
        await self.state.close_stored_position(event.position)
        
        return True

    async def handle_exit_received(self, event: ExitSignal) -> bool:
        if isinstance(event, ExitLongSignalReceived) or isinstance(event, ExitShortSignalReceived):
            signal = event.signal
        else:
            signal = event.position.signal
        
        position = await self.state.retrieve_position(signal)

        if position and self.can_close_position(event, position):
            closed_position = position.close().update_prices(event.exit_price)
            
            await self.state.update_stored_position(closed_position)

            await self.dispatcher.dispatch(PositionCloseRequested(closed_position))
            
            return True
        
        return False
    
    @staticmethod
    def can_close_position(event, position: Position) -> bool:
        if position.side == PositionSide.LONG and isinstance(event, ExitLongSignalReceived):
            return position.entry_price < event.exit_price
        
        if position.side == PositionSide.SHORT and isinstance(event, ExitShortSignalReceived):
            return position.entry_price > event.exit_price
        
        if isinstance(event, RiskThresholdBreached) and position.side == event.position.side:
            return True
        
        return False