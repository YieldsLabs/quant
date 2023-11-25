from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.pulse.base import Pulse, PulseType


@dataclass(frozen=True)
class DumbPulse(Pulse):
    type: PulseType = PulseType.Dumb
    period: Parameter = StaticParameter(10.0)
