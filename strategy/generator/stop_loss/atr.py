from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import StopLoss, StopLossType


@dataclass(frozen=True)
class AtrStopLoss(StopLoss):
    type: StopLossType = StopLossType.Atr
    smooth: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(14.0)
    factor: Parameter = StaticParameter(1.618)
