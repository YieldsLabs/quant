from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DiZeroCrossSignal(Signal):
    type: SignalType = SignalType.DiZeroCross
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
