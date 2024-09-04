from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class NvolPulse(Pulse):
    type: PulseType = PulseType.Nvol
    smooth: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(14.0)
