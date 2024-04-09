import logging
from typing import Union

from core.actors import Actor
from core.commands.broker import AdjustPosition, ClosePosition, OpenPosition
from core.events.position import (
    BrokerPositionAdjusted,
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.events.risk import RiskAdjustRequested
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.position import GetClosePosition, GetOpenPosition

logger = logging.getLogger(__name__)


PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class MarketOrderActor(Actor):
    _EVENTS = [PositionInitialized, RiskAdjustRequested, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__(symbol, timeframe)

    def pre_receive(self, event: PositionEventType):
        event = event.position.signal if hasattr(event, "position") else event
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    async def on_receive(self, event: PositionEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            RiskAdjustRequested: self._adjust_position,
            PositionCloseRequested: self._close_position,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        await self.ask(OpenPosition(current_position))

        order = await self.ask(GetOpenPosition(current_position))

        current_position = current_position.add_order(order)

        logger.info(f"Position to Open: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionOpened(current_position))

    async def _adjust_position(self, event: RiskAdjustRequested):
        current_position, entry_price = event.position, event.adjust_price

        logger.debug(f"To Adjust Position: {current_position}, adjust: {entry_price}")

        await self.ask(AdjustPosition(current_position, entry_price))

        order = await self.ask(GetOpenPosition(current_position))

        current_position = current_position.add_order(order)

        logger.info(f"Adjusted Position: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionAdjusted(current_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.debug(f"To Close Position: {current_position}")

        await self.ask(ClosePosition(current_position, event.exit_price))

        order = await self.ask(GetClosePosition(current_position))

        current_position = current_position.add_order(order)

        logger.info(f"Closed Position: {current_position}")

        await self.tell(BrokerPositionClosed(current_position))
