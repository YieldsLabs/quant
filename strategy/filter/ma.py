from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter


@dataclass(frozen=True)
class MovingAverageFilter(Indicator):
    type: MovingAverageType = MovingAverageType.SMA
    period: Parameter = RandomParameter(100.0, 200.0, 10.0)

    @property
    def parameters(self):
        return [int(self.period.value)]

