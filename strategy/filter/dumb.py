from dataclasses import dataclass
from typing import Any

from core.models.indicator import Indicator


@dataclass(frozen=True)
class DumbFilter(Indicator):
    type: Any = Any
    @property
    def parameters(self):
        return []
