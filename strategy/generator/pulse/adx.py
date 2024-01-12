from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter

from .base import Pulse, PulseType


@dataclass(frozen=True)
class AdxPulse(Pulse):
    type: PulseType = PulseType.Adx
    adx_period: Parameter = StaticParameter(14.0)
    di_period: Parameter = StaticParameter(20.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
