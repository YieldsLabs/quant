from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value


@dataclass
class Order:
    side: OrderSide
    price: float
    size: float
    stop_loss: Optional[float]
    id: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())

    def to_dict(self):
        return asdict(self)