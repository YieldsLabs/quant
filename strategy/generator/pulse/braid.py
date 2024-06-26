from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class BraidPulse(Pulse):
    type: PulseType = PulseType.Braid
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    fast_period: Parameter = StaticParameter(3.0)
    slow_period: Parameter = StaticParameter(14.0)
    open_period: Parameter = StaticParameter(7.0)
    strength: Parameter = StaticParameter(40.0)
    atr_period: Parameter = StaticParameter(14.0)
