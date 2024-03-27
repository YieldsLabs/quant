from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Signal, SignalType


@dataclass(frozen=True)
class ViCrossSignal(Signal):
    type: SignalType = SignalType.ViCross
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(2.0)
