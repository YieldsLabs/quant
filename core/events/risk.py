from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.event import EventGroup
from core.models.entity.position import Position

from ._base import Event


@dataclass(frozen=True)
class RiskEvent(Event):
    position: Position
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=EventGroup.risk), init=False
    )


@dataclass(frozen=True)
class RiskThresholdBreached(RiskEvent):
    pass
