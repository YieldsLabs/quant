import logging
from typing import Union

from core.actors import Actor
from core.commands.broker import ClosePosition, OpenPosition
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.position import GetClosePosition, GetOpenPosition

logger = logging.getLogger(__name__)


PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class MarketOrderActor(Actor):
    _EVENTS = [PositionInitialized, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__(symbol, timeframe, strategy)

    def pre_receive(self, event: PositionEventType):
        event = event.position.signal if hasattr(event, "position") else event
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    async def on_receive(self, event: PositionEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            PositionCloseRequested: self._close_position,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.info(f"New Position: {current_position}")

        await self.ask(OpenPosition(current_position))

        logger.info("Get Open Position")

        order = await self.ask(GetOpenPosition(current_position))

        current_position = current_position.add_order(order)

        logger.info(f"Position to Open: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionOpened(current_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.info(f"To Close Position: {current_position}")

        await self.ask(ClosePosition(current_position, event.exit_price))

        order = await self.ask(GetClosePosition(current_position))

        current_position = current_position.add_order(order)

        logger.info(f"Closed Position: {current_position}")

        await self.tell(BrokerPositionClosed(current_position))
