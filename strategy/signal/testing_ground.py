from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TestingGroundSignal(Signal):
    type: SignalType = SignalType.TestGround
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = StaticParameter(100.0)
