from dataclasses import dataclass
from typing import Any, List

from .base import Query

from ..models.symbol import Symbol


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