from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple

from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)

from .ohlcv import OHLCV
from .order import Order, OrderStatus
from .signal import Signal


class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Position:
    signal: Signal
    side: PositionSide
    size: float
    entry_price: float
    risk_strategy: AbstractPositionRiskStrategy
    take_profit_strategy: AbstractPositionTakeProfitStrategy
    orders: Tuple[Order] = ()
    closed: bool = False
    stop_loss_price: Optional[float] = None
    take_profit_price: Optional[float] = None
    open_timestamp: float = field(default_factory=lambda: 0)
    closed_timestamp: float = field(default_factory=lambda: 0)
    last_modified: float = field(default_factory=lambda: datetime.now().timestamp())
    exit_price: float = field(default_factory=lambda: 0.0000001)

    @property
    def trade_time(self) -> int:
        return abs(int(self.closed_timestamp - self.open_timestamp))

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        factor = 1 if self.side == PositionSide.LONG else -1

        return factor * (self.exit_price - self.entry_price) * self.size

    def add_order(self, order: Order) -> "Position":
        if self.closed:
            return

        last_modified = datetime.now().timestamp()
        orders = (*self.orders, order)

        if order.status == OrderStatus.PENDING:
            return replace(self, orders=orders, last_modified=last_modified)

        if order.status == OrderStatus.EXECUTED:
            return replace(
                self,
                orders=orders,
                entry_price=order.price,
                size=order.size,
                last_modified=last_modified,
            )

        if order.status == OrderStatus.CLOSED:
            return replace(
                self,
                closed=True,
                orders=orders,
                exit_price=order.price,
                closed_timestamp=last_modified,
                last_modified=last_modified,
            )

        if order.status == OrderStatus.FAILED:
            return replace(
                self,
                closed=True,
                orders=orders,
                exit_price=self.entry_price,
                closed_timestamp=last_modified,
                last_modified=last_modified,
            )

    def next(self, ohlcv: OHLCV) -> "Position":
        next_stop_loss = self.risk_strategy.next(
            self.side,
            self.entry_price,
            self.take_profit_price,
            self.stop_loss_price,
            ohlcv,
        )

        return replace(self, stop_loss_price=next_stop_loss)

    def __post_init__(self):
        if self.stop_loss_price:
            object.__setattr__(
                self,
                "take_profit_price",
                round(
                    self.take_profit_strategy.next(
                        self.entry_price, self.stop_loss_price
                    ),
                    self.signal.symbol.price_precision,
                ),
            )

    def to_dict(self):
        return {
            "signal": self.signal.to_dict(),
            "side": str(self.side),
            "size": self.size,
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
        return f"Position(signal={self.signal}, side={self.side}, size={self.size}, entry_price={self.entry_price}, exit_price={self.exit_price}, take_profit_price={self.take_profit_price}, stop_loss_price={self.stop_loss_price}, trade_time={self.trade_time}, closed={self.closed})"
