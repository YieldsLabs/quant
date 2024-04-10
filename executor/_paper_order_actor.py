import asyncio
import logging
from collections import deque
from enum import Enum, auto
from typing import Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    BrokerPositionAdjusted,
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.events.risk import RiskAdjustRequested
from core.models.ohlcv import OHLCV
from core.models.order import Order, OrderStatus, OrderType
from core.models.position import Position
from core.models.side import PositionSide
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
    _EVENTS = [
        NewMarketDataReceived,
        PositionInitialized,
        RiskAdjustRequested,
        PositionCloseRequested,
    ]

    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__(symbol, timeframe)
        self.lock = asyncio.Lock()
        self.tick_buffer = deque(maxlen=15)

    def pre_receive(self, event: OrderEventType):
        event = event.position.signal if hasattr(event, "position") else event
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    async def on_receive(self, event: OrderEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            RiskAdjustRequested: self._adjust_position,
            PositionCloseRequested: self._close_position,
            NewMarketDataReceived: self._update_tick,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        size = current_position.size
        side = current_position.side
        fill_price = await self._determine_fill_price(
            side, current_position.entry_price
        )

        if (
            side == PositionSide.LONG and current_position.stop_loss_price > fill_price
        ) or (
            side == PositionSide.SHORT and current_position.stop_loss_price < fill_price
        ):
            order = Order(
                status=OrderStatus.FAILED,
                type=OrderType.PAPER,
                price=fill_price,
                size=size,
            )
        else:
            order = Order(
                status=OrderStatus.EXECUTED,
                type=OrderType.PAPER,
                fee=fill_price * size * current_position.signal.symbol.taker_fee,
                price=fill_price,
                size=size,
            )

        current_position = current_position.add_order(order)

        logger.debug(f"Position to Open: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionOpened(current_position))

    async def _adjust_position(self, event: RiskAdjustRequested):
        current_position = event.position

        logger.debug(f"To Adjust Position: {current_position}")

        total_value = (current_position.size * current_position.entry_price) + (
            current_position.size * event.adjust_price
        )

        size = current_position.size + current_position.size
        fill_price = total_value / size

        if (
            current_position.side == PositionSide.LONG
            and current_position.stop_loss_price > current_position.take_profit_price
        ) or (
            current_position.side == PositionSide.SHORT
            and current_position.stop_loss_price < current_position.take_profit_price
        ):
            logger.error(f"Wrong Adjust: {current_position}")
            return
        else:
            order = Order(
                status=OrderStatus.EXECUTED,
                type=OrderType.PAPER,
                fee=fill_price * size * current_position.signal.symbol.taker_fee,
                price=fill_price,
                size=size,
            )

            current_position = current_position.add_order(order)

            logger.info(f"Adjusted Position: {current_position}")

            await self.tell(BrokerPositionAdjusted(current_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.debug(f"To Close Position: {current_position}")

        fill_price = await self._determine_fill_price(
            current_position.side, event.exit_price
        )
        price = self._calculate_closing_price(current_position, fill_price)
        size = current_position.size

        order = Order(
            status=OrderStatus.CLOSED,
            type=OrderType.PAPER,
            fee=price * size * current_position.signal.symbol.taker_fee,
            price=price,
            size=size,
        )

        next_position = current_position.add_order(order)

        logger.debug(f"Closed Position: {next_position}")

        await self.tell(BrokerPositionClosed(next_position))

    async def _update_tick(self, event: NewMarketDataReceived):
        async with self.lock:
            self.tick_buffer.append(event.ohlcv)

    async def _determine_fill_price(
        self, side: PositionSide, event_price: float
    ) -> float:
        async with self.lock:
            last_tick = self.tick_buffer[-1]

            direction = self._intrabar_price_movement(last_tick)
            high, low = last_tick.high, last_tick.low

            in_bar = low <= event_price <= high

            if side == PositionSide.LONG and direction == PriceDirection.OHLC:
                return event_price if in_bar else high
            elif side == PositionSide.SHORT and direction == PriceDirection.OLHC:
                return event_price if in_bar else low
            else:
                return last_tick.close

    @staticmethod
    def _intrabar_price_movement(tick: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(tick.open - tick.high) < abs(tick.open - tick.low)
            else PriceDirection.OLHC
        )

    @staticmethod
    def _calculate_closing_price(position: Position, fill_price: float) -> float:
        if position.side == PositionSide.LONG:
            return max(
                min(fill_price, position.take_profit_price),
                position.stop_loss_price,
            )
        else:
            return min(
                max(fill_price, position.take_profit_price),
                position.stop_loss_price,
            )
