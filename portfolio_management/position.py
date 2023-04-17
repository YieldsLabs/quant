from typing import List, Optional

from core.events.order import Order
from core.events.position import PositionSide
from core.timeframes import Timeframes


class Position:
    def __init__(self, symbol: str, timeframe: Timeframes, strategy: str, side: PositionSide, size: float, entry: float, stop_loss: Optional[float] = None, take_profit: Optional[float] = None):
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy = strategy
        self.size = size
        self.side = side
        self.entry_price = entry
        self.exit_price = entry
        self.stop_loss_price = stop_loss
        self.take_profit_price = take_profit
        self.orders: List[Order] = []
        self.closed = False

    def add_order(self, order):
        self.orders.append(order)
        
    def close_position(self, exit_price):
        if self.closed:
            return
        self.closed = True
        self.exit_price = exit_price

    def calculate_pnl(self):
        if not self.closed:
            return None

        if self.side == PositionSide.LONG:
            pnl = (self.exit_price - self.entry_price) * self.size
        elif self.side == PositionSide.SHORT:
            pnl = (self.entry_price - self.exit_price) * self.size

        return pnl