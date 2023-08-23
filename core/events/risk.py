from dataclasses import dataclass, field

from .base_event import Event, EventMeta

from ..models.strategy import Strategy
from ..models.position import PositionSide


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    strategy: Strategy
    side: PositionSide
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
