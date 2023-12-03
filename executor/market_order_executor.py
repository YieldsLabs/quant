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
from core.models.order import Order, OrderStatus
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.position import GetOpenPosition

logger = logging.getLogger(__name__)


PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class MarketOrderExecutor(Actor):
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
        position = event.position
        size = position.size

        logger.info(f"New Position: {position}")

        await self.ask(OpenPosition(position))

        broker_position = await self.ask(GetOpenPosition(position))

        if not broker_position:
            order = Order(status=OrderStatus.FAILED, price=0, size=0)
        else:
            filled_size = broker_position["position_size"]

            if size != filled_size:
                logger.info(f"Partially filled Position: {filled_size}")

            order = Order(
                status=OrderStatus.EXECUTED,
                size=broker_position["position_size"],
                price=broker_position["entry_price"],
            )

        next_position = position.add_order(order)

        logger.info(f"Opened Position: {next_position}")

        await self.tell(BrokerPositionOpened(next_position))

    async def _close_position(self, event: PositionCloseRequested):
        position = event.position

        await self.ask(ClosePosition(position))

        order = Order(
            status=OrderStatus.CLOSED,
            price=event.exit_price,
            size=position.size,
        )

        next_position = position.add_order(order)

        logger.info(f"Closed Position: {next_position}")

        await self.tell(BrokerPositionClosed(next_position))
