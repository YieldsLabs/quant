from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class MA3CrossSignal(BaseSignal):
    type: SignalType = SignalType.Ma3Cross
    smoothing: MovingAverageType = MovingAverageType.SMA
    short_period: Parameter = RandomParameter(5.0, 50.0, 5.0)
    medium_period: Parameter = RandomParameter(50.0, 100.0, 5.0)
    long_period: Parameter = RandomParameter(100.0, 200.0, 10.0)

    @property
    def parameters(self):
        return [
            self.smoothing,
            self.short_period,
            self.medium_period,
            self.long_period,
        ]
