import asyncio
import logging
from enum import Enum, auto
from typing import Optional, Union

from core.actors import StrategyActor
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
from core.queries.copilot import EvaluateSignal

OrderEventType = Union[
    NewMarketDataReceived, PositionInitialized, PositionCloseRequested
]

logger = logging.getLogger(__name__)


class PriceDirection(Enum):
    OHLC = auto()
    OLHC = auto()


class PaperOrderActor(StrategyActor):
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
        for _ in range(4):
            async for next_bar in self.repository.find_next_bar(
                self.symbol, self.timeframe, curr_bar
            ):
                return next_bar
            await asyncio.sleep(0.001)

        return None

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position

        logger.info(f"New Position: {current_position}")

        risk_level = await self.ask(EvaluateSignal(current_position.signal))

        logger.info(f"Risk Level: {risk_level}")

        entry_order = current_position.entry_order()
        next_bar = await self._find_next_bar(current_position.signal_bar)

        price = self._find_open_price(current_position, entry_order, next_bar)
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

        price = self._find_close_price(current_position, exit_order)
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

        logger.info(f"Closed Position: {next_position}")

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

        return self._find_fill_price(position.side, bar, order.price)

    def _find_close_price(
        self, position: Position, order: Order, bar: Optional[OHLCV] = None
    ) -> float:
        if bar is None:
            bar = position.risk_bar

        return self._find_fill_price(position.side, bar, order.price)

    @staticmethod
    def _intrabar_price_movement(bar: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(bar.open - bar.high) < abs(bar.open - bar.low)
            else PriceDirection.OLHC
        )
