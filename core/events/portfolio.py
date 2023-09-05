from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.symbol import Symbol
from ..models.strategy import Strategy
from ..models.portfolio import Performance
from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class PortfolioEvent(Event):
    strategy: Strategy
    timeframe: Timeframe
    symbol: Symbol
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=8, group=EventGroup.portfolio), init=False)


@dataclass(frozen=True)
class PortfolioPerformanceUpdated(PortfolioEvent):
    performance: Performance

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            'symbol': str(self.symbol),
            'timeframe': str(self.timeframe),
            'strategy': str(self.strategy),
            'performance': self.performance.to_dict()
        }

        return {**parent_dict, **current_dict}

