import logging
from typing import Union

from core.actors import StrategyActor
from core.commands.broker import ClosePosition, OpenPosition
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.mixins import EventHandlerMixin
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.position import GetClosePosition, GetOpenPosition

logger = logging.getLogger(__name__)


PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class MarketOrderActor(StrategyActor, EventHandlerMixin):
    _EVENTS = [PositionInitialized, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__(symbol, timeframe)
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

    async def on_receive(self, event: PositionEventType):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(PositionInitialized, self._execute_order)
        self.register_handler(PositionCloseRequested, self._close_position)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        await self.ask(OpenPosition(current_position))

        filled_order = await self.ask(GetOpenPosition(current_position))

        current_position = current_position.fill_order(filled_order)

        logger.info(f"Position to Open: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionOpened(current_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.debug(f"To Close Position: {current_position}")

        await self.ask(ClosePosition(current_position))

        order = await self.ask(GetClosePosition(current_position))

        current_position = current_position.fill_order(order)

        logger.info(f"Closed Position: {current_position}")

        await self.tell(BrokerPositionClosed(current_position))
