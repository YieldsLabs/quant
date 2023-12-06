from dataclasses import dataclass

from core.models.order import Order
from core.models.position import Position
from core.queries.base import Query


@dataclass(frozen=True)
class GetOpenPosition(Query[Order]):
    position: Position


@dataclass(frozen=True)
class GetClosePosition(Query[Order]):
    position: Position
