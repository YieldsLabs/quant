from dataclasses import dataclass, field

from core.models.portfolio import Performance
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class PortfolioEvent(Event):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=8, group=EventGroup.portfolio),
        init=False,
    )


@dataclass(frozen=True)
class PortfolioPerformanceUpdated(PortfolioEvent):
    performance: Performance

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "symbol": str(self.symbol),
            "timeframe": str(self.timeframe),
            "strategy": str(self.strategy),
            "performance": self.performance.to_dict(),
        }

        return {**parent_dict, **current_dict}
