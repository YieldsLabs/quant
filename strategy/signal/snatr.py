from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import Parameter, StaticParameter


@dataclass(frozen=True)
class SNATRSignal(BaseSignal):
    atr_period: Parameter = StaticParameter(60.0)
    atr_smoothing_period: Parameter = StaticParameter(13.0)
    lower_barrier: Parameter = StaticParameter(0.2)
    upper_barrier: Parameter = StaticParameter(0.8)

    @property
    def parameters(self):
        return [
            self.atr_period,
            self.atr_smoothing_period,
            self.lower_barrier,
            self.upper_barrier,
        ]
