from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class TsiCrossSignal(Signal):
    type: SignalType = SignalType.TsiCross
    long_period: Parameter = StaticParameter(25.0)
    short_period: Parameter = StaticParameter(13.0)
    signal_period: Parameter = StaticParameter(13.0)