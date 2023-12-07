from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class RocFlipSignal(Signal):
    type: SignalType = SignalType.RocFlip
    period: Parameter = StaticParameter(9.0)
