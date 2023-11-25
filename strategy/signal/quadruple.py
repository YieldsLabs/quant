from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class QuadrupleSignal(Signal):
    type: SignalType = SignalType.Quadruple
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(40.0, 60.0, 10.0)
