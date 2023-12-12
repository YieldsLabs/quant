import asyncio
import logging
from enum import Enum, auto
from typing import Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.ohlcv import OHLCV
from core.models.order import Order, OrderStatus
from core.models.position import PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

OrderEventType = Union[
    NewMarketDataReceived, PositionInitialized, PositionCloseRequested
]

logger = logging.getLogger(__name__)


class PriceDirection(Enum):
    OHLC = auto()
    OLHC = auto()


class PaperOrderActor(Actor):
    _EVENTS = [NewMarketDataReceived, PositionInitialized, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__(symbol, timeframe, strategy)
        self.lock = asyncio.Lock()
        self.last_tick = None

    def pre_receive(self, event: OrderEventType):
        event = event.position.signal if hasattr(event, "position") else event
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    async def on_receive(self, event: OrderEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            PositionCloseRequested: self._close_position,
            NewMarketDataReceived: self._update_tick,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        fill_price = self._determine_fill_price(current_position.side)
        size = current_position.size

        order = Order(
            status=OrderStatus.EXECUTED,
            price=fill_price,
            size=size,
        )

        next_position = current_position.add_order(order)

        logger.debug(f"Opened Position: {next_position}")

        await self.tell(BrokerPositionOpened(next_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.debug(f"To Close Position: {current_position}")

        fill_price = self._determine_fill_price(current_position.side)
        size = current_position.size

        order = Order(
            status=OrderStatus.CLOSED,
            price=fill_price,
            size=size,
        )

        next_position = current_position.add_order(order)

        logger.debug(f"Closed Position: {next_position}")

        await self.tell(BrokerPositionClosed(next_position))

    async def _update_tick(self, event: NewMarketDataReceived):
        async with self.lock:
            self.last_tick = event.ohlcv

    @staticmethod
    def _intrabar_price_movement(tick: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(tick.open - tick.high) < abs(tick.open - tick.low)
            else PriceDirection.OLHC
        )

    def _determine_fill_price(self, side: PositionSide) -> float:
        direction = self._intrabar_price_movement(self.last_tick)

        if side == PositionSide.LONG and direction == PriceDirection.OHLC:
            return self.last_tick.high
        elif side == PositionSide.SHORT and direction == PriceDirection.OLHC:
            return self.last_tick.low
        else:
            return self.last_tick.close
