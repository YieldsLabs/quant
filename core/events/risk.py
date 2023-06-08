from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from .base_event import Event, EventMeta
from .ohlcv import OHLCV
from ..position import PositionSide
from ..timeframe import Timeframe


class RiskType(Enum):
    BREAK_EVEN = auto()


@dataclass(frozen=True)
class RiskEvaluate(Event):
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
class RiskThresholdBreached(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    side: PositionSide
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))
