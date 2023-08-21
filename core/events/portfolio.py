from dataclasses import dataclass, field

from .base_event import Event, EventMeta

from ..models.portfolio import AdvancedPortfolioPerformance, BasicPortfolioPerformance


@dataclass(frozen=True)
class PortfolioPerformanceUpdated(Event):
    strategy: str
    basic: BasicPortfolioPerformance
    advanced: AdvancedPortfolioPerformance
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=5))
