from dataclasses import dataclass, field
import uuid
from ..event_dispatcher import Event
from ..timeframe import Timeframe


@dataclass(frozen=True)
class StrategyEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    entry: float
    stop_loss: float
    take_profit: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass(frozen=True)
class GoLong(StrategyEvent):
    pass

@dataclass(frozen=True)
class GoShort(StrategyEvent):
    pass