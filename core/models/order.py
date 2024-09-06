import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum, auto


class OrderStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"
    CLOSED = "closed"


class OrderType(Enum):
    MARKET = auto()
    PAPER = auto()


@dataclass(frozen=True)
class Order:
    status: OrderStatus
    price: float
    size: float
    type: OrderType = field(default=OrderType.MARKET)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    fee: float = field(default_factory=lambda: 0.0)

    def to_dict(self):
        return asdict(self)
