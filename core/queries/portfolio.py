from dataclasses import dataclass, field
from typing import List

from core.events._base import EventMeta
from core.groups.query import QueryGroup
from core.models.entity.portfolio import Performance
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Query


@dataclass(frozen=True)
class GetPortfolioRank(Query[List[Strategy]]):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=QueryGroup.portfolio),
        init=False,
    )


@dataclass(frozen=True)
class GetPortfolioPerformance(Query[Performance]):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=QueryGroup.portfolio),
        init=False,
    )
