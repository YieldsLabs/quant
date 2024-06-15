from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import SmoothATR

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class AtrStopLoss(StopLoss):
    type: StopLossType = StopLossType.Atr
    smooth: Parameter = CategoricalParameter(SmoothATR)
    period: Parameter = StaticParameter(14.0)
    factor: Parameter = StaticParameter(1.618)
