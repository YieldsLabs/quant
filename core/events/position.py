from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..timeframe import Timeframe
from ..event_dispatcher import Event

class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value

@dataclass
class PositionEvent(Event):
    symbol: str
    timeframe: Timeframe
    size: float
    entry: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class OpenLongPosition(PositionEvent):
    pass

@dataclass
class OpenShortPosition(PositionEvent):
   pass

@dataclass
class ClosePosition(Event):
    symbol: str
    timeframe: Timeframe
    exit_price: float

@dataclass
class ClosedPosition(ClosePosition):
    pass