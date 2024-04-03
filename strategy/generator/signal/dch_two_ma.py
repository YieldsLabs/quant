from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class Dch2MaSignal(Signal):
    type: SignalType = SignalType.Dch2Ma
    dch_period: Parameter = StaticParameter(20.0)
    ma: Parameter = CategoricalParameter(MovingAverageType)
    fast_period: Parameter = RandomParameter(10.0, 50.0, 10.0)
    slow_period: Parameter = RandomParameter(40.0, 60.0, 10.0)
