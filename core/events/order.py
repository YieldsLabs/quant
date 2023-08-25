from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.position import Position
from ..models.order import Order


@dataclass(frozen=True)
class OrderFilled(Event):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))