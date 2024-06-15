from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class YzPulse(Pulse):
    type: PulseType = PulseType.Yz
    period: Parameter = StaticParameter(21.0)
    smooth_signal: Parameter = StaticParameter(Smooth.SMA)
    period_signal: Parameter = StaticParameter(9.0)
