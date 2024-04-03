from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class CcFlipSignal(Signal):
    type: SignalType = SignalType.CcFlip
    fast_period: Parameter = StaticParameter(11.0)
    slow_period: Parameter = StaticParameter(14.0)
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    smooth_period: Parameter = StaticParameter(20.0)
