import asyncio
from typing import Union

from core.commands.account import AccountUpdate
from core.commands.actor import PositionRiskActorStart, PositionRiskActorStop
from core.commands.position import PositionClose, PositionOpen, PositionUpdate
from core.event_decorators import command_handler, event_handler
from core.events.backtest import BacktestEnded
from core.events.position import LongPositionOpened, ShortPositionOpened
from core.events.order import OrderFilled
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position
from core.models.side import PositionSide
from core.interfaces.abstract_position_manager import AbstractPositionManager
from core.queries.position import PositionBySignal, PositionActive

from .position_state_machine import PositionStateMachine


class PositionManager(AbstractPositionManager):
    def __init__(self, position_factory: AbstractPositionFactory, initial_account_size: int = 1000):
        super().__init__()
        self.account_size = initial_account_size
        self.position_factory = position_factory
        self.sm = PositionStateMachine(self)

    async def is_event_stale(self, signal, event) -> bool:
        position = await self.dispatcher.query(PositionBySignal(signal))

        return position and position.last_modified > event.meta.timestamp

    @command_handler(AccountUpdate)
    async def _update_account(self, command: AccountUpdate):
        self.account_size = command.amount

    @event_handler(GoLongSignalReceived)
    async def _on_go_long(self, event: GoLongSignalReceived):
        if not await self.dispatcher.query(PositionActive(event.signal)):
            await self.sm.process_event(event.signal, event)

    @event_handler(GoShortSignalReceived)
    async def _on_go_short(self, event: GoShortSignalReceived):
        if not await self.dispatcher.query(PositionActive(event.signal)):
            await self.sm.process_event(event.signal, event)

    @event_handler(ExitLongSignalReceived)
    async def _on_exit_long(self, event: ExitLongSignalReceived):
        if await self.is_event_stale(event.signal, event):
            return
        
        if await self.dispatcher.query(PositionActive(event.signal)):
            await self.sm.process_event(event.signal, event)

    @event_handler(ExitShortSignalReceived)
    async def _on_exit_short(self, event: ExitShortSignalReceived):
        if await self.is_event_stale(event.signal, event):
            return
        
        if await self.dispatcher.query(PositionActive(event.signal)):
            await self.sm.process_event(event.signal, event)
    
    @event_handler(RiskThresholdBreached)
    async def _on_exit_risk(self, event: RiskThresholdBreached):
        if await self.is_event_stale(event.signal, event):
            return
        
        if await self.dispatcher.query(PositionActive(event.signal)):
            await self.sm.process_event(event.signal, event)

    @event_handler(OrderFilled)
    async def _on_order_filled(self, event: OrderFilled):
        if await self.is_event_stale(event.position.signal, event):
            return
        
        if await self.dispatcher.query(PositionActive(event.position.signal)):
            await self.sm.process_event(event.position.signal, event)

    @event_handler(BacktestEnded)
    async def _on_order_filled(self, event: BacktestEnded):
        if await self.is_event_stale(event, event):
            return
        
        if await self.dispatcher.query(PositionActive(event)):
            await self.sm.process_event(event, event)

    async def handle_open_position(self, event: Union[GoLongSignalReceived, GoShortSignalReceived]) -> bool:
        position_side = PositionSide.LONG if isinstance(event, GoLongSignalReceived) else PositionSide.SHORT
        
        account_size = self.account_size

        position = self.position_factory.create_position(
            event.signal,
            position_side,
            account_size,
            event.entry_price,
            event.stop_loss
        )

        await self.dispatcher.execute(PositionOpen(position)),
        await self.dispatcher.dispatch(self.create_open_position_event(position)),
        await self.dispatcher.execute(PositionRiskActorStart(position))

        return True

    async def handle_order_filled(self, event: OrderFilled) -> bool:
        await self.dispatcher.execute(PositionUpdate(event.position))

        return True

    async def handle_exit(self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached]) -> bool:
        print('Exit')
        position = await self.dispatcher.query(PositionBySignal(event.signal))

        if position and self.can_close_position(event, position):
            closed_position = position.close().update_prices(event.exit_price)
            
            
            await self.dispatcher.execute(PositionClose(closed_position)),
            await self.dispatcher.execute(PositionRiskActorStop(closed_position))
            
            return True
        
        return False
    
    async def handle_backtest_end(self, event: BacktestEnded) -> bool:
        position = await self.dispatcher.query(PositionBySignal(event))

        if position:
            closed_position = position.close().update_prices(event.exit_price)
            
            await asyncio.gather(
                self.dispatcher.execute(PositionClose(closed_position)),
                self.dispatcher.execute(PositionRiskActorStop(closed_position))
            )
            
            return True
        
        return False


    def create_open_position_event(self, position: Position) -> Union[LongPositionOpened, ShortPositionOpened]:
        if position.side == PositionSide.LONG:
            return LongPositionOpened(position)
        else:
            return ShortPositionOpened(position)

    def can_close_position(self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached], position: Position) -> bool:
        position_side = position.side

        if isinstance(event, ExitLongSignalReceived) and (position_side == PositionSide.LONG):
            if position.entry_price < event.exit_price:
                return True

        if isinstance(event, ExitShortSignalReceived) and (position_side == PositionSide.SHORT):
            if position.entry_price > event.exit_price:
                return True

        if isinstance(event, RiskThresholdBreached) and (position_side == event.side):
            return True

        return False