from dataclasses import dataclass, field

from .base_event import Event, EventMeta

from ..models.position import PositionSide
from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    side: PositionSide
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
