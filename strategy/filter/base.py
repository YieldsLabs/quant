from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class FilterType(Enum):
    Adx = "Adx"
    Dumb = "Dumb"
    Ma = "Ma"
    Rsi = "Rsi"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseFilter(Indicator):
    type: FilterType
