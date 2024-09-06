from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import SmoothATR

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class AtrStopLoss(StopLoss):
    type: StopLossType = StopLossType.Atr
    smooth: Parameter = StaticParameter(SmoothATR.SMMA)
    period: Parameter = StaticParameter(6.0)
    factor: Parameter = StaticParameter(0.68)
