from dataclasses import dataclass, field
from typing import List

from core.events.base import EventMeta
from core.models.entity.position import Position
from core.models.symbol import Symbol

from .base import Query, QueryGroup


@dataclass(frozen=True)
class GetSymbols(Query[List[Symbol]]):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=QueryGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class GetSymbol(Query[Symbol]):
    symbol: Symbol
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=QueryGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class HasPosition(Query[bool]):
    position: Position
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=QueryGroup.broker),
        init=False,
    )
