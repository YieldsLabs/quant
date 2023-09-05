from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.ohlcv import OHLCV
from ..models.position import Position


@dataclass(frozen=True)
class RiskEvent(Event):
    position: Position
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1, group=EventGroup.risk), init=False)


@dataclass(frozen=True)
class RiskThresholdBreached(RiskEvent):
    exit_price: float