from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class HighLowSignal(Signal):
    type: SignalType = SignalType.HighLow
    period: Parameter = StaticParameter(3.0)
