from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe
from ..models.ohlcv import OHLCV


@dataclass(frozen=True)
class NewMarketDataReceived(Event):
    symbol: Symbol
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=5))
