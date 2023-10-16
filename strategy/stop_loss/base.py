from dataclasses import dataclass
from typing import Any, Tuple

from core.models.indicator import Indicator
from core.models.stop_loss import StopLossType


@dataclass(frozen=True)
class BaseStopLoss(Indicator):
    type: StopLossType

    def parameters(self) -> Tuple[Any, ...]:
        return []
