from dataclasses import dataclass
from typing import List

from .base import Query

from ..models.signal import Signal


@dataclass(frozen=True)
class GetTopSignals(Query[List[Signal]]):
    num: int = 5


@dataclass(frozen=True)
class GetTotalPnL(Query[float]):
    signal: Signal