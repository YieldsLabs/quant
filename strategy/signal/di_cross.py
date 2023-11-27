from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DiCrossSignal(Signal):
    type: SignalType = SignalType.DiCross
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
    signal_period: Parameter = RandomParameter(4.0, 8.0, 1.0)
