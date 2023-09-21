from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe
from ..models.ohlcv import OHLCV


@dataclass(frozen=True)
class MarketEvent(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4, group=EventGroup.market), init=False)


@dataclass(frozen=True)
class NewMarketDataReceived(MarketEvent):
    symbol: Symbol
    timeframe: Timeframe
    ohlcv: OHLCV
    closed: bool
