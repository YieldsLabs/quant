from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ExitType(Enum):
    Ast = "Ast"
    Dumb = "Dumb"
    Ch = "Ch"
    HighLow = "HighLow"
    Pattern = "Pattern"
    Ma = "Ma"
    Rsi = "Rsi"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Exit(Indicator):
    type: ExitType
