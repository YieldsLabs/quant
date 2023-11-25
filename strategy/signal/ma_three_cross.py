from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, RandomParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MA3CrossSignal(Signal):
    type: SignalType = SignalType.Ma3Cross
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    short_period: Parameter = RandomParameter(5.0, 50.0, 5.0)
    medium_period: Parameter = RandomParameter(50.0, 100.0, 5.0)
    long_period: Parameter = RandomParameter(100.0, 200.0, 10.0)
