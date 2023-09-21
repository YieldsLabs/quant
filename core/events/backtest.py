from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.strategy import Strategy
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


@dataclass(frozen=True)
class BacktestEvent(Event):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=6, group=EventGroup.backtest), init=False)


@dataclass(frozen=True)
class BacktestStarted(BacktestEvent):
    strategy: Strategy
    

@dataclass(frozen=True)
class BacktestEnded(BacktestEvent):
    exit_price: float