from dataclasses import asdict, dataclass
from ..event_dispatcher import Event
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

@dataclass
class OHLCVEvent(Event):
    symbol: str
    timeframe: Timeframe
    ohlcv: OHLCV
