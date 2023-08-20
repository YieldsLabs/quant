from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .timeframe import Timeframe


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value


class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value


@dataclass
class Order:
    side: OrderSide
    price: float
    size: float
    id: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())

    def to_dict(self):
        return asdict(self)


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

    @property
    def strategy_id(self) -> str:
        return f'{self.symbol}_{self.timeframe}{self.strategy}'

    @property
    def closed_key(self) -> str:
        return f"{self.symbol}_{self.closed_timestamp}"
    
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
