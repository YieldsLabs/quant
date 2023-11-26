from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from strategy.pulse.base import Pulse, PulseType


@dataclass(frozen=True)
class CHOPPulse(Pulse):
    type: PulseType = PulseType.Chop
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(14.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
