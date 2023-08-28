from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.position import PositionSide
from ..models.signal import Signal


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    signal: Signal
    side: PositionSide
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
