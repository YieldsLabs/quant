from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class TrixCrossSignal(Signal):
    type: SignalType = SignalType.TrixCross
    period: Parameter = StaticParameter(7.0)
    signal_period: Parameter = StaticParameter(9.0)
