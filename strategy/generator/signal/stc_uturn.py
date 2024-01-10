from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class StcUTurnSignal(Signal):
    type: SignalType = SignalType.StcUturn
    fast_period: Parameter = StaticParameter(23.0)
    slow_period: Parameter = StaticParameter(50.0)
    cycle: Parameter = StaticParameter(12.0)
    d_first: Parameter = StaticParameter(3.0)
    d_second: Parameter = StaticParameter(3.0)
