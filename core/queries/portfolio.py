from dataclasses import dataclass
from typing import List

from core.models.signal import Signal
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Query


@dataclass(frozen=True)
class GetTopStrategy(Query[List[Strategy]]):
    num: int = 5


@dataclass(frozen=True)
class GetEquity(Query[float]):
    signal: Signal


@dataclass(frozen=True)
class GetFitness(Query[float]):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
