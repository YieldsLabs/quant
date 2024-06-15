from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class ChopPulse(Pulse):
    type: PulseType = PulseType.Chop
    period: Parameter = StaticParameter(9.0)
    smooth_atr: Parameter = StaticParameter(Smooth.SMMA)
    period_atr: Parameter = StaticParameter(1.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
