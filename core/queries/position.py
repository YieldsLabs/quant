from dataclasses import dataclass, field

from core.events.base import EventMeta
from core.models.order import Order
from core.models.position import Position
from core.queries.base import Query, QueryGroup


@dataclass(frozen=True)
class GetOpenPosition(Query[Order]):
    position: Position
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=QueryGroup.position),
        init=False,
    )


@dataclass(frozen=True)
class GetClosePosition(Query[Order]):
    position: Position
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=QueryGroup.broker),
        init=False,
    )
