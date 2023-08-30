from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class OrderStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"


@dataclass(frozen=True)
class Order:
    status: OrderStatus
    price: float
    size: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))

    def to_dict(self):
        return asdict(self)