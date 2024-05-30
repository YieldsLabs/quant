from dataclasses import dataclass, field

from core.events.base import EventMeta
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.ta import TechAnalysis
from core.models.timeframe import Timeframe

from .base import Query, QueryGroup


@dataclass(frozen=True)
class NextBar(Query[OHLCV]):
    symbol: Symbol
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=6, group=QueryGroup.market),
        init=False,
    )


@dataclass(frozen=True)
class PrevBar(Query[OHLCV]):
    symbol: Symbol
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=6, group=QueryGroup.market),
        init=False,
    )


@dataclass(frozen=True)
class TA(Query[TechAnalysis]):
    symbol: Symbol
    timeframe: Timeframe
    ohlcv: OHLCV
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=7, group=QueryGroup.ta),
        init=False,
    )
