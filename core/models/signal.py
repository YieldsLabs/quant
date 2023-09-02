from dataclasses import dataclass
from enum import Enum

from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe


class SignalSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value.upper()

@dataclass(frozen=True)
class Signal:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    side: SignalSide

    def __str__(self) -> str:
        return f"{self.symbol.name}_{self.timeframe}_{self.side}{self.strategy}"
    
    def __repr__(self) -> str:
        return f"Signal(symbol={self.symbol}, timeframe={self.timeframe}, side={self.side}, strategy={self.strategy})"
    
    def __hash__(self) -> int:
        return hash((self.symbol, self.timeframe, self.strategy, self.side))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Signal):
            return NotImplemented

        return self.symbol == other.symbol and self.side == other.side and self.timeframe == other.timeframe and self.strategy == other.strategy
    
    def to_dict(self):
        return {
            'symbol': str(self.symbol),
            'timeframe': str(self.timeframe),
            'strategy': str(self.strategy),
            'side': str(self.side)
        }
    

    