from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter


@dataclass(frozen=True)
class TestingGroundSignal(Indicator):
    ma: MovingAverageType = MovingAverageType.EMA
    period: Parameter = RandomParameter(60.0, 180.0, 10.0)

    @property
    def parameters(self):
        return [self.ma, self.period]
