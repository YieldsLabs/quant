from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class VoPulse(Pulse):
    type: PulseType = PulseType.Vo
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    fast_period: Parameter = StaticParameter(7.0)
    slow_period: Parameter = StaticParameter(13.0)
