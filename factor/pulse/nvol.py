from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class NvolPulse(Pulse):
    type: PulseType = PulseType.Nvol
    smooth: Parameter = CategoricalParameter(Smooth)
    period: Parameter = StaticParameter(14.0)
