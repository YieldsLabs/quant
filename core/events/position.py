from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from typing import Optional

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
    timestamp: int = datetime.now().timestamp()

@dataclass(frozen=True)
class OpenLongPosition(PositionEvent):
   pass

@dataclass(frozen=True)
class OpenShortPosition(PositionEvent):
   pass

@dataclass(frozen=True)
class ClosePosition(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float
    timestamp: int = datetime.now().timestamp()

@dataclass(frozen=True)
class ClosedPosition(ClosePosition):
    pass