from dataclasses import dataclass

from core.models.position import Position
from core.queries.base import Query


@dataclass(frozen=True)
class GetOpenPosition(Query[Position]):
    position: Position
