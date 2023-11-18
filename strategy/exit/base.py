from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ExitType(Enum):
    Dumb = "Dumb"
    Pattern = "Pattern"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseExit(Indicator):
    type: ExitType
