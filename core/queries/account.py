from dataclasses import dataclass

from core.queries.base import Query


@dataclass(frozen=True)
class GetBalance(Query[float]):
    currency: str = "USDT"
