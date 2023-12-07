from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class BopFlipSignal(Signal):
    type: SignalType = SignalType.BopFlip
    smoothing_period: Parameter = StaticParameter(14.0)
