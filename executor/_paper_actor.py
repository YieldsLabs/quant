import logging
from enum import Enum, auto
from typing import Optional, Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.interfaces.abstract_market_repository import AbstractMarketRepository
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
        PositionCloseRequested,
    ]

    def __init__(
        self, symbol: Symbol, timeframe: Timeframe, repository: AbstractMarketRepository
    ):
        super().__init__(symbol, timeframe)
        self.repository = repository

    def pre_receive(self, event: OrderEventType):
        event = event.position.signal if hasattr(event, "position") else event
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    async def on_receive(self, event: OrderEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            PositionCloseRequested: self._close_position,
            NewMarketDataReceived: self._update_bar,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _update_bar(self, event: NewMarketDataReceived):
        await self.repository.upsert(self.symbol, self.timeframe, event.ohlcv)

    async def _find_next_bar(self, curr_bar: OHLCV) -> Optional[OHLCV]:
        async for next_bar in self.repository.find_next_bar(
            self.symbol, self.timeframe, curr_bar
        ):
            return next_bar

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.debug(f"New Position: {current_position}")

        next_bar = await self._find_next_bar(current_position.signal_bar)

        entry_order = current_position.entry_order()

        if next_bar:
            price = self._find_fill_price(current_position, next_bar, entry_order)
        else:
            price = self._find_fill_price(
                current_position, current_position.signal_bar, entry_order
            )
            logger.warn(f"Will use current bar with price: {price}")

        size = entry_order.size
        fee = current_position.theo_taker_fee(size, price)

        order = Order(
            status=OrderStatus.EXECUTED,
            type=OrderType.PAPER,
            size=size,
            price=price,
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

        size = exit_order.size
        price = self._find_closing_price(
            current_position, current_position.risk_bar, exit_order
        )

        fee = current_position.theo_taker_fee(size, price)

        order = Order(
            status=OrderStatus.CLOSED,
            type=OrderType.PAPER,
            size=size,
            price=price,
            fee=fee,
        )

        next_position = current_position.fill_order(order)

        logger.debug(f"Closed Position: {next_position}")

        await self.tell(BrokerPositionClosed(next_position))

    def _find_fill_price(self, position: Position, bar: OHLCV, order: Order) -> float:
        direction = self._intrabar_price_movement(bar)

        high, low = bar.high, bar.low
        in_bar = low <= order.price <= high

        if position.side == PositionSide.LONG and direction == PriceDirection.OHLC:
            return order.price if in_bar else high
        elif position.side == PositionSide.SHORT and direction == PriceDirection.OLHC:
            return order.price if in_bar else low
        else:
            return bar.close

    def _find_closing_price(
        self, position: Position, bar: OHLCV, price: float
    ) -> float:
        fill_price = self._find_fill_price(position, bar, price)

        if position.side == PositionSide.LONG:
            return max(min(fill_price, position.take_profit), position.stop_loss)
        else:
            return min(max(fill_price, position.take_profit), position.stop_loss)

    @staticmethod
    def _intrabar_price_movement(tick: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(tick.open - tick.high) < abs(tick.open - tick.low)
            else PriceDirection.OLHC
        )
