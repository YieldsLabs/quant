from dataclasses import dataclass, field
from typing import List, Optional

from core.events._base import EventMeta
from core.groups.query import QueryGroup
from core.models.cap import CapType
from core.models.exchange import ExchangeType
from core.models.symbol import Symbol

from ._base import Query


@dataclass(frozen=True)
class GetSymbols(Query[List[Symbol]]):
    exchange: ExchangeType
    cap: Optional[CapType] = None
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=QueryGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class GetSimularSymbols(Query[List[Symbol]]):
    symbol: Symbol
    exchange: ExchangeType
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=QueryGroup.broker),
        init=False,
    )
