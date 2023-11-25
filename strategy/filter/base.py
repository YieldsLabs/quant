from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class FilterType(Enum):
    Apo = "Apo"
    Bop = "Bop"
    Braid = "Braid"
    Dumb = "Dumb"
    Fib = "Fib"
    Eis = "Eis"
    Ribbon = "Ribbon"
    Rsi = "Rsi"
    Tii = "Tii"
    Stoch = "Stoch"
    Supertrend = "Supertrend"
    Macd = "Macd"
    Kst = "Kst"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Filter(Indicator):
    type: FilterType
