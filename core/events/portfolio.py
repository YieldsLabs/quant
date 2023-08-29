from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.signal import Signal
from ..models.portfolio import Performance


@dataclass(frozen=True)
class PortfolioPerformanceUpdated(Event):
    signal: Signal
    performance: Performance
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=7))
