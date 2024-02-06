from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class BopFlipSignal(Signal):
    type: SignalType = SignalType.BopFlip
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    smoothing_period: Parameter = StaticParameter(14.0)
