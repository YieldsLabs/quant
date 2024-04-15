from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class RocZeroCrossSignal(Signal):
    type: SignalType = SignalType.RocZeroCross
    period: Parameter = StaticParameter(9.0)
