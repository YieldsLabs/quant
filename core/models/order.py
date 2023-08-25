from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional

from .side import OrderSide


@dataclass(frozen=True)
class Order:
    side: OrderSide
    price: float
    size: float
    id: Optional[str] = None
    timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))

    def to_dict(self):
        return asdict(self)