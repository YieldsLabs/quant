from dataclasses import dataclass
from typing import List

from .base import Query

from ..models.signal import Signal
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe
from ..models.strategy import Strategy


@dataclass(frozen=True)
class GetTopStrategy(Query[List[Strategy]]):
    num: int = 5


@dataclass(frozen=True)
class GetTotalPnL(Query[float]):
    signal: Signal

@dataclass(frozen=True)
class GetFitness(Query[float]):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
