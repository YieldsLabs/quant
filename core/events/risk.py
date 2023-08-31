from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.position import Position


@dataclass(frozen=True)
class RiskEvent(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1, group=EventGroup.risk), init=False)


@dataclass(frozen=True)
class RiskThresholdBreached(RiskEvent):
    position: Position
    exit_price: float
