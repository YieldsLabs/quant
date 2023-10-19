from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class StopLossType(Enum):
    Atr = "Atr"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseStopLoss(Indicator):
    type: StopLossType
