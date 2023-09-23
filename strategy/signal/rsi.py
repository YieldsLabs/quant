from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import Parameter, RandomParameter, StaticParameter


@dataclass(frozen=True)
class RSINautralitySignal(Indicator):
    rsi_period: Parameter = StaticParameter(21.0)
    threshold: Parameter = RandomParameter(3.0, 7.0, 1.0)

    @property
    def parameters(self):
        return [
            self.rsi_period,
            self.threshold, 
        ]