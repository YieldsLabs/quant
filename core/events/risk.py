from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.event import EventGroup
from core.models.entity.signal import Signal

from ._base import Event


@dataclass(frozen=True)
class RiskEvent(Event):
    signal: Signal
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=EventGroup.risk), init=False
    )


@dataclass(frozen=True)
class RiskLongThresholdBreached(RiskEvent):
    pass


@dataclass(frozen=True)
class RiskShortThresholdBreached(RiskEvent):
    pass
