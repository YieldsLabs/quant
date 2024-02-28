from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter

from .base import Signal, SignalType


@dataclass(frozen=True)
class MaSurpassSignal(Signal):
    type: SignalType = SignalType.MaSurpass
    ma: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = RandomParameter(150.0, 200.0, 10.0)
