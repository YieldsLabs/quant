from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from strategy.stop_loss.base import BaseStopLoss, StopLossType


@dataclass(frozen=True)
class ATRStopLoss(BaseStopLoss):
    type: StopLossType = StopLossType.Atr
    period: Parameter = StaticParameter(14.0)
    multi: Parameter = RandomParameter(0.85, 2, 0.05)
