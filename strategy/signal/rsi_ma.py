from dataclasses import dataclass
from inspect import Parameter

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter


@dataclass(frozen=True)
class RSIMovingAverageSignal(Indicator):
    rsi_period: Parameter = StaticParameter(2.0)
    lower_barrier: Parameter = RandomParameter(5.0, 15.0, 1.0)
    upper_barrier: Parameter = RandomParameter(90.0, 95.0, 1.0)
    ma: MovingAverageType = MovingAverageType.EMA
    period: Parameter = RandomParameter(50.0, 100.0, 5.0)

    @property
    def parameters(self):
        return [
            self.rsi_period,
            self.lower_barrier,
            self.upper_barrier,
            self.ma,
            self.period,
        ]
