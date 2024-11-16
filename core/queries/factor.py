from dataclasses import dataclass, field
from typing import Tuple

from core.events.meta import EventMeta
from core.groups.query import QueryGroup

from ._base import Query


@dataclass(frozen=True)
class GetGeneration(Query[Tuple[list, float]]):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=6, group=QueryGroup.factor),
        init=False,
    )
