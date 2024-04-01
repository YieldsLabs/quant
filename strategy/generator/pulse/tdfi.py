from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class TdfiPulse(Pulse):
    type: PulseType = PulseType.Tdfi
    smooth_type: Parameter = StaticParameter(Smooth.ZLEMA)
    period: Parameter = StaticParameter(14.0)
    n: Parameter = StaticParameter(3.0)
