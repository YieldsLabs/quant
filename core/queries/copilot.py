from dataclasses import dataclass, field
from typing import List

from core.events.base import EventMeta
from core.models.ohlcv import OHLCV
from core.models.risk_type import SessionRiskType
from core.models.side import PositionSide
from core.models.signal import Signal
from core.models.signal_risk import SignalRisk
from core.models.ta import TechAnalysis

from .base import Query, QueryGroup


@dataclass(frozen=True)
class EvaluateSignal(Query[SignalRisk]):
    signal: Signal
    prev_bar: OHLCV
    ta: TechAnalysis
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=QueryGroup.copilot),
        init=False,
    )


@dataclass(frozen=True)
class EvaluateSession(Query[SessionRiskType]):
    side: PositionSide
    session: List[OHLCV]
    ta: TechAnalysis
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=QueryGroup.copilot),
        init=False,
    )
