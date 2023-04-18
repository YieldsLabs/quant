from dataclasses import dataclass
from ..event_dispatcher import Event
from ..timeframe import Timeframe


@dataclass
class StrategyEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    entry: float
    stop_loss: float
    take_profit: float

@dataclass
class GoLong(StrategyEvent):
   pass

@dataclass
class GoShort(StrategyEvent):
    pass