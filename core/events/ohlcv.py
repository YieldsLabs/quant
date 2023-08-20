from dataclasses import asdict, dataclass, field

from .base_event import Event, EventMeta
from ..timeframe import Timeframe


@dataclass
class OHLCV:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class NewMarketDataReceived(Event):
    symbol: str
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3))
