from dataclasses import dataclass
from typing import Any

from core.models.indicator import Indicator
from core.models.parameter import Parameter, StaticParameter


@dataclass(frozen=True)
class SNATRIndicator(Indicator):
    type: Any = Any
    atr_period: Parameter = StaticParameter(60.0)
    atr_smoothing_period: Parameter = StaticParameter(13.0)

    @property
    def parameters(self):
        return [int(self.atr_period.value), int(self.atr_smoothing_period.value)]