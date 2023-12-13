from dataclasses import dataclass, field

from core.events.base import EventMeta
from core.queries.base import Query, QueryGroup


@dataclass(frozen=True)
class GetBalance(Query[float]):
    currency: str = "USDT"
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=4, group=QueryGroup.account),
        init=False,
    )
