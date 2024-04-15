from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class AoZeroCrossSignal(Signal):
    type: SignalType = SignalType.AoZeroCross
    fast_period: Parameter = StaticParameter(5.0)
    slow_period: Parameter = StaticParameter(34.0)
