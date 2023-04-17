from dataclasses import asdict, dataclass
from ..event_dispatcher import Event

from core.timeframes import Timeframes


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
    timeframe: Timeframes
    ohlcv: OHLCV