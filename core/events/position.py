from dataclasses import dataclass, field
from typing import List, Optional

from .ohlcv import OHLCV
from .base_event import Event, EventMeta
from ..timeframe import Timeframe
from ..position import Order, Position, PositionSide


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
class ActivePositionOpened(Event):
    symbol: str
    timeframe: Timeframe
    side: PositionSide
    size: float
    entry: float
    stop_loss: Optional[float]
    risk_reward_ratio: float
    risk_per_trade: float
    ohlcv: OHLCV
    strategy: str
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class PositionClosed(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class ClosedPositionUpdated(Event):
    strategy_id: str
    position: List[Position]
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
