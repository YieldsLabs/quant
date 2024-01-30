from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter

from .base import Signal, SignalType


@dataclass(frozen=True)
class StochCrossSignal(Signal):
    type: SignalType = SignalType.StochCross
    period: Parameter = RandomParameter(13.0, 16.0, 1.0)
    k_period: Parameter = RandomParameter(1.0, 5.0, 1.0)
    d_period: Parameter = RandomParameter(3.0, 5.0, 1.0)
