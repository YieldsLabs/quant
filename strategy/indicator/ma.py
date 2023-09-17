from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter


@dataclass(frozen=True)
class MovingAverageIndicator(Indicator):
    type: MovingAverageType = MovingAverageType.SMA
    long_period: Parameter = RandomParameter(100.0, 200.0, 10.0)

    @property
    def parameters(self):
        return [int(self.long_period.value)]

