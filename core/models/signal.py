from dataclasses import dataclass

from .side import PositionSide
from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe


@dataclass(frozen=True)
class Signal:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy

    def __str__(self) -> str:
        return f"{self.symbol.name}_{self.timeframe}_{self.strategy}"
    
    def __hash__(self) -> int:
        return hash(self.symbol) ^ hash(self.timeframe) ^ hash(self.strategy)