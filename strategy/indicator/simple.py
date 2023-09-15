from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import Parameter, RandomParameter


@dataclass(frozen=True)
class SimpleIndicator(Indicator):
    period: Parameter = RandomParameter(150.0, 200.0, 10.0)

    @property
    def parameters(self):
        return [int(self.period.value)]