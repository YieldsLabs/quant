from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.pulse.base import Pulse, PulseType


@dataclass(frozen=True)
class OSCPulse(Pulse):
    type: PulseType = PulseType.Osc
    short_period: Parameter = StaticParameter(5.0)
    long_period: Parameter = StaticParameter(10.0)
