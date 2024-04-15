from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MacdZeroCrossSignal(Signal):
    type: SignalType = SignalType.MacdZeroCross
    smooth_type: Parameter = CategoricalParameter(Smooth)
    fast_period: Parameter = StaticParameter(12.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
