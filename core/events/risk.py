from dataclasses import dataclass, field
from enum import Enum, auto

from .base_event import Event, EventMeta
from ..position import PositionSide
from ..timeframe import Timeframe


class RiskType(Enum):
    BREAK_EVEN = auto()


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    side: PositionSide
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
