from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class DCH2MovingAverageSignal(BaseSignal):
    type: SignalType = SignalType.Dch2Ma
    dch_period: Parameter = StaticParameter(20.0)
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    short_period: Parameter = RandomParameter(10.0, 50.0, 10.0)
    long_period: Parameter = RandomParameter(40.0, 60.0, 10.0)
