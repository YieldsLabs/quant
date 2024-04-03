from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class AoFlipSignal(Signal):
    type: SignalType = SignalType.AoFlip
    fast_period: Parameter = StaticParameter(5.0)
    slow_period: Parameter = StaticParameter(34.0)
