from dataclasses import dataclass, field
from typing import List, Optional

from .base_event import Event, EventMeta
from ..timeframe import Timeframe
from ..position import Order, Position


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
class PositionReadyToClose(Event):
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


@dataclass(frozen=True)
class PositionClosedUpdated(Event):
    strategy_id: str
    position: List[Position]
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
