from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class DchStopLoss(StopLoss):
    type: StopLossType = StopLossType.Dch
    period: Parameter = StaticParameter(21.0)
    factor: Parameter = StaticParameter(0.3)
