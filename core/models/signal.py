from dataclasses import dataclass
from enum import Enum

from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe

class SignalSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class Signal:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    side: SignalSide

    def __str__(self) -> str:
        return f"{self.symbol.name}_{self.timeframe}_{self.strategy}"
    
    def __hash__(self) -> int:
        return hash(self.symbol) ^ hash(self.timeframe) ^ hash(self.strategy)