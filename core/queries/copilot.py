from dataclasses import dataclass, field
from typing import List

from core.events._base import EventMeta
from core.groups.query import QueryGroup
from core.models.entity.ohlcv import OHLCV
from core.models.entity.signal import Signal
from core.models.entity.signal_risk import SignalRisk
from core.models.risk_type import SessionRiskType
from core.models.side import PositionSide
from core.models.ta import TechAnalysis

from ._base import Query


@dataclass(frozen=True)
class EvaluateSignal(Query[SignalRisk]):
    signal: Signal
    prev_bar: List[OHLCV]
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
        default_factory=lambda: EventMeta(priority=1, group=QueryGroup.copilot),
        init=False,
    )
