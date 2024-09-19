from dataclasses import field

from core.models.side import SignalSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Entity
from .ohlcv import OHLCV


@Entity
class Signal:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    side: SignalSide
    ohlcv: OHLCV
    entry: float = field(default_factory=lambda: 0.0)
    exit: float = field(default_factory=lambda: 0.0)
    stop_loss: float = field(default_factory=lambda: 0.0)

    def __hash__(self) -> int:
        return hash((self.symbol, self.timeframe, self.strategy, self.side))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Signal):
            return NotImplemented

        return (
            self.symbol == other.symbol
            and self.side == other.side
            and self.timeframe == other.timeframe
            and self.strategy == other.strategy
        )

    def __str__(self) -> str:
        return f"{self.symbol.name}_{self.timeframe}_{self.side}{self.strategy}"
