from dataclasses import dataclass, field
from typing import Optional

from .base_event import Event, EventMeta

from ..models.position import Order
from ..models.strategy import Strategy

@dataclass(frozen=True)
class OrderFilled(Event):
    strategy: Strategy
    order: Order
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class PositionEvent(Event):
    strategy: Strategy
    size: float
    entry: float
    stop_loss: Optional[float]
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=7))


@dataclass(frozen=True)
class LongPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class ShortPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionClosed(Event):
    strategy: Strategy
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3))