from dataclasses import dataclass
from typing import List

from .base import Query

from ..models.signal import Signal
from ..models.position import Position


@dataclass(frozen=True)
class PositionActive(Query[bool]):
    signal: Signal

@dataclass(frozen=True)
class PositionBySignal(Query[Position | None]):
    signal: Signal

@dataclass(frozen=True)
class PositionAll(Query[List[Position]]):
    pass