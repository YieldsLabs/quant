from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DchMa2BreakoutSignal(Signal):
    type: SignalType = SignalType.DchMa2Breakout
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    dch_period: Parameter = StaticParameter(20.0)
    ma: Parameter = CategoricalParameter(MovingAverageType)
    fast_period: Parameter = RandomParameter(10.0, 50.0, 10.0)
    slow_period: Parameter = RandomParameter(40.0, 60.0, 10.0)
