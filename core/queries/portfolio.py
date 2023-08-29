from dataclasses import dataclass
from typing import List, Tuple

from core.models.position import Position
from core.models.strategy import Strategy
from core.queries.base import Query


@dataclass(frozen=True)
class GetTopStrategy(Query[List[Strategy]]):
    num: int = 5


@dataclass(frozen=True)
class GetOpenPositions(Query[List[Position]]):
    strategy: Strategy


@dataclass(frozen=True)
class GetTotalPnL(Query[float]):
    strategy: Strategy


@dataclass(frozen=True)
class GetEquity(Query[List[Tuple[int, float]]]):
    strategy: Strategy


@dataclass(frozen=True)
class GetDrawdown(Query[List[Tuple[int, float]]]):
    strategy: Strategy