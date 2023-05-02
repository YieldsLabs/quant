from dataclasses import dataclass, field
from .base_event import Event, EventMeta
from .ohlcv import OHLCV
from .position import PositionSide

from ..timeframe import Timeframe


@dataclass(frozen=True)
class RiskEvaluate(Event):
    symbol: str
    timeframe: Timeframe
    side: PositionSide
    size: float
    entry: float
    stop_loss: float
    take_profit: float
    risk: float
    ohlcv: OHLCV
    strategy: str
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class RiskExit(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
