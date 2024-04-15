from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CfoZeroCrossSignal(Signal):
    type: SignalType = SignalType.CfoZeroCross
    period: Parameter = StaticParameter(14.0)
