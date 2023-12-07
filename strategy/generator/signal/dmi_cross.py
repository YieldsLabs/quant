from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class DmiCrossSignal(Signal):
    type: SignalType = SignalType.DmiCross
    adx_period: Parameter = StaticParameter(12.0)
    di_period: Parameter = StaticParameter(12.0)
