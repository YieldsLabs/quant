from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import SmoothATR

from .base import Pulse, PulseType


@dataclass(frozen=True)
class ChopPulse(Pulse):
    type: PulseType = PulseType.Chop
    period: Parameter = StaticParameter(9.0)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(1.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
