from dataclasses import dataclass
from datetime import datetime
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
    timestamp: int = datetime.now().timestamp()

    def __hash__(self):
        return hash((self.symbol, self.timeframe, self.strategy, self.entry, self.stop_loss, self.take_profit, self.timestamp))

@dataclass(frozen=True)
class GoLong(StrategyEvent):
    pass

@dataclass(frozen=True)
class GoShort(StrategyEvent):
    pass