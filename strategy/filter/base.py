from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple

from core.models.indicator import Indicator


class FilterType(Enum):
    Dumb = "Dumb"
    Ma = "Ma"
    Rsi = "Rsi"


@dataclass(frozen=True)
class BaseFilter(Indicator):
    type: FilterType

    def parameters(self) -> Tuple[Any, ...]:
        return []
