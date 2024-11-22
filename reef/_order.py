import time
from dataclasses import dataclass, field, replace

import numpy as np

from core.models.datasource_type import DataSourceType
from core.models.symbol import Symbol


@dataclass(order=True, frozen=True, slots=True)
class PQOrder:
    order_id: str = field(compare=False)
    symbol: Symbol = field(compare=False)
    datasource: DataSourceType = field(compare=False)
    timestamp: float = field(default_factory=lambda: time.time(), compare=True)
    ttl: float = field(
        default_factory=lambda: np.mean(np.random.exponential(3, size=1000)),
        compare=False,
    )

    def copy(self) -> "PQOrder":
        return replace(self, ttl=np.mean(np.random.exponential(3, size=1000)))
