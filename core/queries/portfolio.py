from dataclasses import dataclass, field
from typing import List

from core.events.base import EventMeta
from core.models.entity.signal import Signal
from core.models.size import PositionSizeType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Query, QueryGroup


@dataclass(frozen=True)
class GetTopStrategy(Query[List[Strategy]]):
    num: int = 5
    positive_pnl: bool = False
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=QueryGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class GetPositionRisk(Query[float]):
    signal: Signal
    type: PositionSizeType
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=QueryGroup.portfolio),
        init=False,
    )


@dataclass(frozen=True)
class GetFitness(Query[float]):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=QueryGroup.broker),
        init=False,
    )
