from dataclasses import dataclass
from typing import List

from .base import Query

from ..models.strategy import Strategy
from ..models.signal import Signal


@dataclass(frozen=True)
class GetTopStrategy(Query[List[Strategy]]):
    num: int = 5


@dataclass(frozen=True)
class GetTotalPnL(Query[float]):
    signal: Signal