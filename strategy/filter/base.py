from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class FilterType(Enum):
    Adx = "Adx"
    Dumb = "Dumb"
    Ma = "Ma"
    Ribbon = "Ribbon"
    Rsi = "Rsi"
    Tii = "Tii"
    Stoch = "Stoch"
    Supertrend = "Supertrend"
    Macd = "Macd"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseFilter(Indicator):
    type: FilterType
