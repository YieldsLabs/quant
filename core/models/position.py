from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import List, Tuple

from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .side import PositionSide
from .signal import Signal


@dataclass(frozen=True)
class Position:
    signal: Signal
    side: PositionSide
    risk_strategy: AbstractPositionRiskStrategy
    take_profit_strategy: AbstractPositionTakeProfitStrategy
    orders: Tuple[Order] = ()
    stop_loss_price: float = field(default_factory=lambda: 0.0000001)
    take_profit_price: float = field(default_factory=lambda: 0.0000001)
    open_timestamp: float = field(default_factory=lambda: 0)
    closed_timestamp: float = field(default_factory=lambda: 0)
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())

    @property
    def trade_time(self) -> int:
        return abs(int(self.closed_timestamp - self.open_timestamp))

    @property
    def closed(self) -> bool:
        closed_orders = [
            order.size for order in self.orders if order.status == OrderStatus.CLOSED
        ]
        closed_size = sum(closed_orders)

        failed_orders = [
            order for order in self.orders if order.status == OrderStatus.FAILED
        ]

        pending_orders = [
            order for order in self.orders if order.status == OrderStatus.PENDING
        ]

        if not closed_orders:
            return False

        return closed_size >= self.filled_size or len(failed_orders) == len(
            pending_orders
        )

    @property
    def adj_count(self) -> int:
        executed_orders = [
            order for order in self.orders if order.status == OrderStatus.EXECUTED
        ]
        return max(
            0,
            len(executed_orders) - 1,
        )

    @property
    def pending_size(self) -> int:
        pending_orders = [
            order.size for order in self.orders if order.status == OrderStatus.PENDING
        ]

        return sum(pending_orders)

    @property
    def pending_price(self) -> int:
        pending_orders = [
            order.price for order in self.orders if order.status == OrderStatus.PENDING
        ]

        return sum(pending_orders) / len(pending_orders) if pending_orders else 0.0

    @property
    def filled_size(self) -> int:
        executed_orders = [
            order.size for order in self.orders if order.status == OrderStatus.EXECUTED
        ]

        return sum(executed_orders)

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        factor = -1 if self.side == PositionSide.SHORT else 1

        return factor * (self.exit_price - self.entry_price) * self.filled_size

    @property
    def fee(self) -> float:
        executed_orders = [
            order.fee for order in self.orders if order.status == OrderStatus.EXECUTED
        ]
        open_fee = sum(executed_orders)

        closed_orders = [
            order.fee for order in self.orders if order.status == OrderStatus.CLOSED
        ]
        closed_fee = sum(closed_orders)

        return open_fee + closed_fee

    @property
    def entry_price(self) -> float:
        executed_orders = [
            order.price for order in self.orders if order.status == OrderStatus.EXECUTED
        ]
        return sum(executed_orders) / len(executed_orders) if executed_orders else 0.0

    @property
    def exit_price(self) -> float:
        closed_orders = [
            order.price for order in self.orders if order.status == OrderStatus.CLOSED
        ]

        return sum(closed_orders) / len(closed_orders) if closed_orders else 0.0

    def add_order(self, order: Order) -> "Position":
        if self.closed:
            return self

        last_modified = datetime.now().timestamp()
        orders = (*self.orders, order)

        if order.status == OrderStatus.PENDING or order.status == OrderStatus.EXECUTED:
            take_profit_price = self.take_profit_strategy.next(
                self.side, order.price, self.stop_loss_price
            )

            return replace(
                self,
                orders=orders,
                last_modified=last_modified,
                take_profit_price=take_profit_price,
            )

        if order.status == OrderStatus.CLOSED or order.status == OrderStatus.FAILED:
            return replace(
                self,
                orders=orders,
                closed_timestamp=last_modified,
                last_modified=last_modified,
            )

    def next(self, ohlcvs: List[Tuple[OHLCV]]) -> "Position":
        next_stop_loss_price, next_take_profit_price = self.risk_strategy.next(
            self.side,
            self.entry_price,
            self.take_profit_price,
            self.stop_loss_price,
            ohlcvs,
        )

        return replace(
            self,
            stop_loss_price=next_stop_loss_price,
            take_profit_price=next_take_profit_price,
        )

    def to_dict(self):
        return {
            "signal": self.signal.to_dict(),
            "side": str(self.side),
            "pending_size": self.pending_size,
            "filled_size": self.filled_size,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "closed": self.closed,
            "stop_loss_price": self.stop_loss_price,
            "take_profit_price": self.take_profit_price,
            "pnl": self.pnl,
            "open_timestamp": self.open_timestamp,
            "trade_time": self.trade_time,
        }

    def __str__(self):
        return f"Position(signal={self.signal}, side={self.side}, pending_size={self.pending_size}, filled_size={self.filled_size}, entry_price={self.entry_price}, exit_price={self.exit_price}, take_profit_price={self.take_profit_price}, stop_loss_price={self.stop_loss_price}, trade_time={self.trade_time}, closed={self.closed})"
