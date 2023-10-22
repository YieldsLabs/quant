from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TestingGroundSignal(BaseSignal):
    type: SignalType = SignalType.TestGround
    smoothing: MovingAverageType = MovingAverageType.SMA
    period: Parameter = StaticParameter(100.0)
