from dataclasses import dataclass
from core.event_dispatcher import Event
from core.events.ohlcv import OHLCV
from core.timeframes import Timeframes


@dataclass
class StrategyEvent(Event):
    symbol: str
    timeframe: Timeframes
    strategy: str
    entry: float
    stop_loss: float
    take_profit: float

@dataclass
class GoLong(StrategyEvent):
   pass

@dataclass
class GoShort(StrategyEvent):
    pass