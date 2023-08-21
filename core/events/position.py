from dataclasses import dataclass, field
from typing import Optional

from .base_event import Event, EventMeta

from ..models.ohlcv import OHLCV
from ..models.timeframe import Timeframe
from ..models.position import Order, PositionSide


@dataclass(frozen=True)
class OrderFilled(Event):
    symbol: str
    timeframe: Timeframe
    order: Order
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class PositionEvent(Event):
    symbol: str
    timeframe: Timeframe
    size: float
    entry: float
    stop_loss: Optional[float]
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class LongPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class ShortPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class ClosePositionPrepared(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class PositionClosed(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))