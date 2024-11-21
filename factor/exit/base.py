from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ExitType(Enum):
    Ast = "Ast"
    Mad = "Mad"
    Dumb = "Dumb"
    HighLow = "HighLow"
    Rsi = "Rsi"
    Ma = "Ma"
    Mfi = "Mfi"
    Trix = "Trix"
    Rex = "Rex"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Exit(Indicator):
    type: ExitType
