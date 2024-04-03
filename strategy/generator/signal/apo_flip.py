from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class ApoFlipSignal(Signal):
    type: SignalType = SignalType.ApoFlip
    fast_period: Parameter = StaticParameter(10.0)
    slow_period: Parameter = StaticParameter(20.0)
