from dataclasses import dataclass, field

from .entity.ohlcv import OHLCV
from .side import SignalSide
from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe


@dataclass(frozen=True)
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

    def to_dict(self):
        return {
            "symbol": str(self.symbol),
            "timeframe": str(self.timeframe),
            "strategy": str(self.strategy),
            "side": str(self.side),
            "ohlcv": self.ohlcv.to_dict(),
            "entry": self.entry,
            "stop_loss": self.stop_loss,
        }

    def __str__(self) -> str:
        return f"{self.symbol.name}_{self.timeframe}_{self.side}{self.strategy}"

    def __repr__(self) -> str:
        return f"Signal({self})"
