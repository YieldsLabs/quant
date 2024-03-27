from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class AdxPulse(Pulse):
    type: PulseType = PulseType.Adx
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    adx_period: Parameter = StaticParameter(15.0)
    di_period: Parameter = StaticParameter(15.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
