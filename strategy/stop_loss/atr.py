from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.stop_loss import StopLossType


@dataclass(frozen=True)
class ATRStopLoss(Indicator):
    type: StopLossType = StopLossType.ATR
    period: Parameter = StaticParameter(14.0)
    multi: Parameter = RandomParameter(0.85, 2, 0.05)

    @property
    def parameters(self):
        return [
            self.type,
            self.period,
            self.multi
        ]