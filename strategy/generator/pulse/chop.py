from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter

from .base import Pulse, PulseType


@dataclass(frozen=True)
class ChopPulse(Pulse):
    type: PulseType = PulseType.Chop
    period: Parameter = StaticParameter(9.0)
    atr_period: Parameter = StaticParameter(1.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
