from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.symbol import Symbol
from ..models.strategy import Strategy
from ..models.portfolio import Performance
from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class PortfolioPerformanceUpdated(Event):
    strategy: Strategy
    timeframe: Timeframe
    symbol: Symbol
    performance: Performance
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=7))
