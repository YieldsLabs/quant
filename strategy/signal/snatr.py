from dataclasses import dataclass
from typing import Any

from core.models.indicator import Indicator
from core.models.parameter import Parameter, StaticParameter


@dataclass(frozen=True)
class SNATRSignal(Indicator):
    atr_period: Parameter = StaticParameter(60.0)
    atr_smoothing_period: Parameter = StaticParameter(13.0)

    @property
    def parameters(self):
        return [
            self.atr_period,
            self.atr_smoothing_period
        ]