from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import Parameter, RandomParameter


@dataclass(frozen=True)
class TestingGroundIndicator(Indicator):
    period: Parameter = RandomParameter(60.0, 180.0, 10.0)

    @property
    def parameters(self):
        return [int(self.period.value)]