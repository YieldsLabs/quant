from dataclasses import dataclass, field
import uuid
from ..event_dispatcher import Event, EventMeta
from ..timeframe import Timeframe


@dataclass(frozen=True)
class StrategyEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    entry: float
    stop_loss: float
    take_profit: float
    meta: EventMeta = field(default_factory=EventMeta)

@dataclass(frozen=True)
class GoLong(StrategyEvent):
    pass

@dataclass(frozen=True)
class GoShort(StrategyEvent):
    pass