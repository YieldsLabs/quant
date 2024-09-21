from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.query import QueryGroup

from ._base import Query


@dataclass(frozen=True)
class GetBalance(Query[float]):
    currency: str = "USDT"
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=4, group=QueryGroup.account),
        init=False,
    )
