from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class AtrStopLoss(StopLoss):
    type: StopLossType = StopLossType.Atr
    period: Parameter = StaticParameter(14.0)
    multi: Parameter = StaticParameter(1.2)
