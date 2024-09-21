from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.query import QueryGroup
from core.models.entity.order import Order
from core.models.entity.position import Position

from ._base import Query


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
