from dataclasses import dataclass
from typing import Any, List

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
    name: str


@dataclass(frozen=True)
class GetOpenPosition(Query[Any]):
    symbol: Symbol
