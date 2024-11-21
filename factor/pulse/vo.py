from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class VoPulse(Pulse):
    type: PulseType = PulseType.Vo
    smooth: Parameter = CategoricalParameter(Smooth)
    period_fast: Parameter = StaticParameter(7.0)
    period_slow: Parameter = StaticParameter(13.0)
