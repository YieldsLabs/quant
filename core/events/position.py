from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.timeframes import Timeframes

from ..event_dispatcher import Event

class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value

@dataclass
class PositionEvent(Event):
    symbol: str
    timeframe: Timeframes
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
    timeframe: Timeframes
    exit_price: float

@dataclass
class ClosedPosition(Event):
    symbol: str
    timeframe: Timeframes
    exit_price: float