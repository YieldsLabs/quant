from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from core.timeframes import Timeframes
from ..event_dispatcher import Event

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value

@dataclass
class Order:
    side: OrderSide
    entry: float
    size: float
    stop_loss: float
    take_profit: Optional[float] = None
    id: Optional[str] = None
    timestamp: int = datetime.now().timestamp()

    def to_dict(self):
        return asdict(self)

@dataclass
class FillOrder(Event):
    symbol: str
    timeframe: Timeframes
    order: Order