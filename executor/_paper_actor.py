import logging
from enum import Enum, auto
from typing import Optional, Union

from core.actors import StrategyActor
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.mixins import EventHandlerMixin
from core.models.entity.ohlcv import OHLCV
from core.models.entity.order import Order
from core.models.order_type import OrderStatus, OrderType
from core.models.position import Position
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.ohlcv import NextBar

OrderEventType = Union[PositionInitialized, PositionCloseRequested]

logger = logging.getLogger(__name__)


class PriceDirection(Enum):
    OHLC = auto()
    OLHC = auto()


class PaperOrderActor(StrategyActor, EventHandlerMixin):
    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__(symbol, timeframe)
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

    async def on_receive(self, event: OrderEventType):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(PositionInitialized, self._execute_order)
        self.register_handler(PositionCloseRequested, self._close_position)

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        entry_order = current_position.entry_order()

        price = self._find_open_price(current_position, entry_order)
        size = entry_order.size
        fee = current_position.theo_taker_fee(size, price)

        order = Order(
            status=OrderStatus.EXECUTED,
            type=OrderType.PAPER,
            price=price,
            size=size,
            fee=fee,
        )

        current_position = current_position.fill_order(order)

        if not current_position.is_valid:
            order = Order(
                status=OrderStatus.FAILED, type=OrderType.PAPER, price=0, size=0
            )

            current_position = current_position.fill_order(order)

        logger.debug(f"Position to Open: {current_position}")

        if current_position.closed:
            await self.tell(BrokerPositionClosed(current_position))
        else:
            await self.tell(BrokerPositionOpened(current_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position

        logger.debug(f"To Close Position: {current_position}")

        exit_order = current_position.exit_order()

        next_bar = await self.ask(
            NextBar(self.symbol, self.timeframe, current_position.risk_bar)
        )

        price = self._find_close_price(current_position, exit_order, next_bar)
        size = exit_order.size
        fee = current_position.theo_taker_fee(size, price)

        order = Order(
            status=OrderStatus.CLOSED,
            type=OrderType.PAPER,
            price=price,
            size=size,
            fee=fee,
        )

        next_position = current_position.fill_order(order)

        logger.debug(f"Closed Position: {next_position}")

        await self.tell(BrokerPositionClosed(next_position))

    def _find_fill_price(self, side: PositionSide, bar: OHLCV, price: float) -> float:
        direction = self._intrabar_price_movement(bar)

        high, low = bar.high, bar.low
        in_bar = low <= price <= high

        if direction == PriceDirection.OHLC:
            if side == PositionSide.LONG:
                return price if in_bar else high
        elif direction == PriceDirection.OLHC:
            if side == PositionSide.SHORT:
                return price if in_bar else low

        return bar.close

    def _find_open_price(
        self, position: Position, order: Order, bar: Optional[OHLCV] = None
    ) -> float:
        if bar is None:
            bar = position.signal_bar

        diff = bar.timestamp - position.signal_bar.timestamp

        if diff > position.signal.timeframe.to_milliseconds():
            logger.warn("The open of the next bar is too far from the previous one.")
            bar = position.signal_bar

        return self._find_fill_price(position.side, bar, order.price)

    def _find_close_price(
        self, position: Position, order: Order, bar: Optional[OHLCV] = None
    ) -> float:
        if bar is None:
            bar = position.risk_bar

        diff = bar.timestamp - position.risk_bar.timestamp

        if diff > position.signal.timeframe.to_milliseconds():
            logger.warn("The close of the next bar is too far from the previous one.")
            bar = position.risk_bar

        return self._find_fill_price(position.side, bar, order.price)

    @staticmethod
    def _intrabar_price_movement(bar: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(bar.open - bar.high) < abs(bar.open - bar.low)
            else PriceDirection.OLHC
        )
