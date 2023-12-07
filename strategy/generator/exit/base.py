from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ExitType(Enum):
    Ast = "Ast"
    Dumb = "Dumb"
    Ce = "Ce"
    HighLow = "HighLow"
    Pattern = "Pattern"
    Ma = "Ma"
    Rsi = "Rsi"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Exit(Indicator):
    type: ExitType
