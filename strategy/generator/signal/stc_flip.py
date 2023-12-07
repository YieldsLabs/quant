from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class StcFlipSignal(Signal):
    type: SignalType = SignalType.StcFlip
    fast_period: Parameter = StaticParameter(32.0)
    slow_period: Parameter = StaticParameter(44.0)
    cycle: Parameter = StaticParameter(17.0)
    d_first: Parameter = StaticParameter(12.0)
    d_second: Parameter = StaticParameter(5.0)
