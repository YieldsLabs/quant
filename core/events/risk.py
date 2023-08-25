from dataclasses import dataclass, field

from core.models.side import PositionSide

from .base import Event, EventMeta

from ..models.signal import Signal


@dataclass(frozen=True)
class RiskThresholdBreached(Event):
    signal: Signal
    side: PositionSide
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
