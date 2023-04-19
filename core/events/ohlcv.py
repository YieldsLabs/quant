from dataclasses import asdict, dataclass
from datetime import datetime
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
    
    def __hash__(self):
        return hash((self.timestamp, self.open, self.high, self.low, self.close, self.volume))

@dataclass(frozen=True)
class OHLCVEvent(Event):
    symbol: str
    timeframe: Timeframe
    ohlcv: OHLCV
    timestamp: int = datetime.now().timestamp()
