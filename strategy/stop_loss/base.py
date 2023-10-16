from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class StopLossType(Enum):
    Atr = "Atr"


@dataclass(frozen=True)
class BaseStopLoss(Indicator):
    type: StopLossType
