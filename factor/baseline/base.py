from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class BaseLineType(Enum):
    Ma = "Ma"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseLine(Indicator):
    type: BaseLineType
