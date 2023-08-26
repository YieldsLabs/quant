from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class BacktestEnded(Event):
    symbol: Symbol
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3))