from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class BopZeroCrossSignal(Signal):
    type: SignalType = SignalType.BopZeroCross
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    smooth_period: Parameter = StaticParameter(14.0)
