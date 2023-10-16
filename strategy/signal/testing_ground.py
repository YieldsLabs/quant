from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TestingGroundSignal(BaseSignal):
    type: SignalType = SignalType.Testground
    smoothing: MovingAverageType = MovingAverageType.EMA
    period: Parameter = RandomParameter(60.0, 180.0, 10.0)

    @property
    def parameters(self):
        return [self.smoothing, self.period]
