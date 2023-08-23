from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .strategy import Strategy
from .order import Order


class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Position:
    strategy: Strategy
    side: PositionSide
    size: float
    entry_price: float
    risk_reward_ratio: float
    risk_per_trade: float
    stop_loss_price: Optional[float] = None
    orders: List[Order] = field(default_factory=list)
    closed: bool = False
    open_timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    closed_timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    exit_price: float = field(default_factory=lambda: 0.0001)

    @property
    def closed_key(self) -> str:
        return f"{self.strategy}_{int(self.closed_timestamp)}"

    @property
    def pnl(self) -> float:
        pnl = 0.0

        if not self.closed:
            return pnl

        if self.side == PositionSide.LONG:
            pnl = (self.exit_price - self.entry_price) * self.size
        elif self.side == PositionSide.SHORT:
            pnl = (self.entry_price - self.exit_price) * self.size

        return pnl

    def add_order(self, order: Order) -> 'Position':
        return replace(self, orders=self.orders + [order])

    def close_position(self, exit_price: float) -> 'Position':
        if self.closed:
            return self

        return replace(
            self, 
            closed=True, 
            closed_timestamp=datetime.now().timestamp(), 
            exit_price=exit_price
        )

    def update_prices(self, execution_price: float) -> 'Position':
        if not self.closed:
            return replace(self, entry_price=execution_price)
        else:
            return replace(self, exit_price=execution_price)