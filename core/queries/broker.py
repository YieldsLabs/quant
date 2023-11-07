from dataclasses import dataclass
from typing import List

from core.models.position import Position
from core.models.symbol import Symbol

from .base import Query


@dataclass(frozen=True)
class GetAccountBalance(Query[float]):
    currency: str = "USDT"


@dataclass(frozen=True)
class GetSymbols(Query[List[Symbol]]):
    pass


@dataclass(frozen=True)
class GetSymbol(Query[Symbol]):
    symbol: str


@dataclass(frozen=True)
class GetOpenPosition(Query[Position]):
    position: Position
