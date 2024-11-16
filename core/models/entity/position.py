import logging
import uuid
from dataclasses import field, replace
from datetime import datetime
from typing import List, Optional, Tuple

from core.models.order_type import OrderStatus
from core.models.side import PositionSide, SignalSide

from ._base import Entity
from .ohlcv import OHLCV
from .order import Order
from .signal import Signal

logger = logging.getLogger(__name__)


@Entity
class Position:
    initial_size: float
    orders: Tuple[Order] = ()
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    signal: Signal = None
    close_signal: Signal = None

    @property
    def side(self) -> Optional[PositionSide]:
        if not self.signal:
            return None

        side = self.signal.side

        if side == SignalSide.BUY:
            return PositionSide.LONG

        if side == SignalSide.SELL:
            return PositionSide.SHORT

    @property
    def open_timestamp(self) -> int:
        open_bar = self.open_bar

        return open_bar.timestamp if open_bar else 0

    @property
    def close_timestamp(self) -> int:
        close_bar = self.close_bar

        return close_bar.timestamp if close_bar else 0

    @property
    def open_bar(self) -> Optional[OHLCV]:
        return self.signal.ohlcv if self.signal else None

    @property
    def close_bar(self) -> Optional[OHLCV]:
        return self.close_signal.ohlcv if self.close_signal else None

    @property
    def trade_time(self) -> int:
        return abs(self.close_timestamp - self.open_timestamp)

    @property
    def closed(self) -> bool:
        if not self.orders:
            return False

        if self.rejected_orders:
            return True

        if not self.closed_orders:
            return False

        order_diff = self._average_size(self.open_orders) - self._average_size(
            self.closed_orders
        )

        return order_diff <= 0

    @property
    def size(self) -> float:
        if self.closed_orders:
            return self._average_size(self.closed_orders)

        if self.open_orders:
            return self._average_size(self.open_orders)

        return 0.0

    @property
    def open_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.EXECUTED]

    @property
    def closed_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.CLOSED]

    @property
    def rejected_orders(self) -> List[Order]:
        return [order for order in self.orders if order.status == OrderStatus.FAILED]

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        factor = -1.0 if self.side == PositionSide.SHORT else 1
        pnl = factor * (self.exit_price - self.entry_price) * self.size

        return pnl

    @property
    def fee(self) -> float:
        return sum([order.fee for order in self.open_orders]) + sum(
            [order.fee for order in self.closed_orders]
        )

    @property
    def entry_price(self) -> float:
        return self._average_price(self.open_orders)

    @property
    def exit_price(self) -> float:
        return self._average_price(self.closed_orders)

    @property
    def is_valid(self) -> bool:
        if self.closed and self.size == 0:
            return False

        if self.closed and self.open_timestamp > self.close_timestamp:
            return False

        return True

    @property
    def entry_order(self) -> Order:
        size = self.initial_size
        price = self.signal.entry

        return Order(
            status=OrderStatus.PENDING,
            size=size,
            price=price,
        )

    @property
    def exit_order(self) -> Order:
        size = self._average_size(self.open_orders) - self._average_size(
            self.closed_orders
        )
        price = self.close_signal.exit

        return Order(
            status=OrderStatus.PENDING,
            size=size,
            price=price,
        )

    def open_position(self, signal: Signal):
        return replace(
            self,
            signal=signal,
        )

    def close_position(self, signal: Signal):
        return replace(
            self,
            close_signal=signal,
        )

    def fill_order(self, order: Order) -> "Position":
        if self.closed:
            return self

        if order.status == OrderStatus.PENDING:
            return self

        orders = (*self.orders, order)

        return replace(
            self,
            orders=orders,
            last_modified=datetime.now().timestamp(),
        )

    def trail(self, next_sl: float) -> "Position":
        return replace(self, _sl=next_sl, last_modified=datetime.now().timestamp())

    def theo_taker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.taker_fee

    def theo_maker_fee(self, size: float, price: float) -> float:
        return size * price * self.signal.symbol.maker_fee

    @staticmethod
    def _average_size(orders: List[Order]) -> float:
        total_size = sum(order.size for order in orders)
        return total_size / len(orders) if orders else 0.0

    @staticmethod
    def _average_price(orders: List[Order]) -> float:
        total_price = sum(order.price for order in orders)
        return total_price / len(orders) if orders else 0.0
