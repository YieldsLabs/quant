from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class DiFlipSignal(Signal):
    type: SignalType = SignalType.DiFlip
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
