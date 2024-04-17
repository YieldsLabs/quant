from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MaCrossSignal(Signal):
    type: SignalType = SignalType.MaCross
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(100.0, 150.0, 10.0)
