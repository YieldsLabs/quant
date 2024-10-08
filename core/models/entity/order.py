import uuid
from dataclasses import field
from datetime import datetime
from typing import Dict

from core.models.order_type import OrderStatus, OrderType

from ._base import Entity


@Entity
class Order:
    status: OrderStatus
    price: float
    size: float
    type: OrderType = field(default=OrderType.MARKET)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: int(datetime.now().timestamp()))
    fee: float = field(default_factory=lambda: 0.0)

    @classmethod
    def from_dict(cls, data: Dict) -> "Order":
        order_status = OrderStatus.from_raw(data["orderStatus"])
        price = float(data["price"])
        size = float(data["qty"])
        order_type = OrderType.from_raw(data["orderType"])
        id = data["orderId"]
        fee = data["closedPnl"]

        return cls(
            status=order_status,
            price=price,
            size=size,
            type=order_type,
            id=id,
            fee=fee,
        )
