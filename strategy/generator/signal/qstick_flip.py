from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class QstickFlipSignal(Signal):
    type: SignalType = SignalType.QstickFlip
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
