from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.position import Position


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    position: Position
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
