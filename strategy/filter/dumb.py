from dataclasses import dataclass
from typing import Any

from core.models.indicator import Indicator


@dataclass(frozen=True)
class DumbFilter(Indicator):
    @property
    def parameters(self):
        return []
