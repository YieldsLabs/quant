from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class AtrStopLoss(StopLoss):
    type: StopLossType = StopLossType.Atr
    period: Parameter = StaticParameter(3.0)
    factor: Parameter = StaticParameter(1.618)
