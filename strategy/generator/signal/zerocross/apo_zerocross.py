from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class ApoZeroCrossSignal(Signal):
    type: SignalType = SignalType.ApoZeroCross
    fast_period: Parameter = StaticParameter(10.0)
    slow_period: Parameter = StaticParameter(20.0)
