from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid

from ..timeframe import Timeframe
from ..event_dispatcher import Event

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
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

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
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass(frozen=True)
class ClosedPosition(ReadyToClosePosition):
    pass