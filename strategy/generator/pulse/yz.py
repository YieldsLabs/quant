from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class YzPulse(Pulse):
    type: PulseType = PulseType.Yz
    period: Parameter = StaticParameter(40.0)
    smooth_signal: Parameter = StaticParameter(Smooth.SMA)
    period_signal: Parameter = StaticParameter(12.0)
