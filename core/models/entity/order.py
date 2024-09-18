import uuid
from dataclasses import dataclass, field
from datetime import datetime

from core.models.order_type import OrderStatus, OrderType

from ._base import Entity


@dataclass(frozen=True)
class Order(Entity):
    status: OrderStatus
    price: float
    size: float
    type: OrderType = field(default=OrderType.MARKET)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    fee: float = field(default_factory=lambda: 0.0)
