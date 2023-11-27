from dataclasses import dataclass
from typing import List

from core.models.symbol import Symbol

from .base import Query


@dataclass(frozen=True)
class GetSymbols(Query[List[Symbol]]):
    pass


@dataclass(frozen=True)
class GetSymbol(Query[Symbol]):
    symbol: str
