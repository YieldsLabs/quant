from dataclasses import asdict, dataclass, field

from .base_event import Event, EventMeta

from ..models.timeframe import Timeframe
from ..models.ohlcv import OHLCV


@dataclass(frozen=True)
class NewMarketDataReceived(Event):
    symbol: str
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3))
