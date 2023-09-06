from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter


@dataclass(frozen=True)
class CrossMovingAverageIndicator(Indicator):
    type: MovingAverageType
    short_period: Parameter = Parameter(5.0, 50.0, 5.0)
    long_period: Parameter = Parameter(50.0, 200.0, 10.0)

    @property
    def parameters(self):
        return (int(self.short_period.value), int(self.long_period.value),)

