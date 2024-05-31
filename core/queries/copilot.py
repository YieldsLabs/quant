from dataclasses import dataclass, field

from core.events.base import EventMeta
from core.models.ohlcv import OHLCV
from core.models.position_risk import PositionRisk
from core.models.risk_type import SessionRiskType, SignalRiskType
from core.models.signal import Signal

from .base import Query, QueryGroup


@dataclass(frozen=True)
class EvaluateSignal(Query[SignalRiskType]):
    signal: Signal
    prev_bar: OHLCV
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=QueryGroup.copilot),
        init=False,
    )


@dataclass(frozen=True)
class EvaluateSession(Query[SessionRiskType]):
    risk: PositionRisk
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=QueryGroup.copilot),
        init=False,
    )
