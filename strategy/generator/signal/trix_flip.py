from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class TrixFlipSignal(Signal):
    type: SignalType = SignalType.TrixFlip
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(7.0)
