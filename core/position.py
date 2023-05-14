from datetime import datetime
from typing import List, Optional

from .events.position import PositionSide, Order
from .timeframe import Timeframe


class Position:
    def __init__(self, symbol: str, timeframe: Timeframe, strategy: str, side: PositionSide, size: float, entry: float, risk_reward_ratio: float, stop_loss: Optional[float] = None):
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy = strategy
        self.size = size
        self.side = side
        self.entry_price = entry
        self.exit_price = entry
        self.stop_loss_price = stop_loss
        self.risk_reward_ratio = risk_reward_ratio
        self.orders: List[Order] = []
        self.closed = False
        self.open_timestamp = datetime.now().timestamp()
        self.closed_timestamp = self.open_timestamp

    def add_order(self, order: Order):
        self.orders.append(order)

    def close_position(self, exit_price):
        if self.closed:
            return
        self.closed = True
        self.closed_timestamp = datetime.now().timestamp()
        self.update_prices(exit_price)

    def update_prices(self, execution_price):
        if not self.closed:
            self.entry_price = execution_price
        else:
            self.exit_price = execution_price

    def calculate_pnl(self) -> float | None:
        if not self.closed:
            return None

        pnl = 0.0

        if self.side == PositionSide.LONG:
            pnl = (self.exit_price - self.entry_price) * self.size
        elif self.side == PositionSide.SHORT:
            pnl = (self.entry_price - self.exit_price) * self.size

        return pnl
