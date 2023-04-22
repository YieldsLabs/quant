from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .ohlcv import OHLCV
from .base_event import Event, EventMeta
from ..timeframe import Timeframe

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value

@dataclass
class Order:
    side: OrderSide
    entry: float
    size: float
    stop_loss: float
    take_profit: Optional[float] = None
    id: Optional[str] = None
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())

    def to_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class FillOrder(Event):
    symbol: str
    timeframe: Timeframe
    order: Order
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))

class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class PositionEvent(Event):
    symbol: str
    timeframe: Timeframe
    size: float
    entry: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))

@dataclass(frozen=True)
class OpenLongPosition(PositionEvent):
   pass

@dataclass(frozen=True)
class OpenShortPosition(PositionEvent):
   pass

@dataclass(frozen=True)
class ReadyToClosePosition(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))

@dataclass(frozen=True)
class ClosedPosition(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))

@dataclass(frozen=True)
class CheckExitConditions(Event):
    symbol: str
    timeframe: Timeframe
    side: PositionSide
    size: float
    entry: float
    stop_loss: float
    take_profit: float
    risk: float
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))