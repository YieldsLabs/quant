from dataclasses import dataclass
from inspect import Parameter

from core.models.indicator import Indicator
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter


@dataclass(frozen=True)
class RSI2xMovingAverageSignal(Indicator):
    rsi_period: Parameter = StaticParameter(2.0)
    lower_barrier: Parameter = RandomParameter(5.0, 15.0, 5.0)
    upper_barrier: Parameter = RandomParameter(80.0, 95.0, 5.0)
    ma: MovingAverageType = MovingAverageType.EMA
    short_period: Parameter = RandomParameter(20.0, 50.0, 1.0)
    long_period: Parameter = RandomParameter(30.0, 50.0, 1.0)

    @property
    def parameters(self):
        return [
            self.rsi_period,
            self.lower_barrier, 
            self.upper_barrier, 
            self.ma,
            self.short_period,
            self.long_period
        ]
