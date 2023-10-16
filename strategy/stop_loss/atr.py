from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.stop_loss import StopLossType
from strategy.stop_loss.base import BaseStopLoss


@dataclass(frozen=True)
class ATRStopLoss(BaseStopLoss):
    type: StopLossType = StopLossType.ATR
    period: Parameter = StaticParameter(14.0)
    multi: Parameter = RandomParameter(0.85, 2, 0.05)

    @property
    def parameters(self):
        return [self.period, self.multi]
