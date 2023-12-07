from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter

from .base import Signal, SignalType


@dataclass(frozen=True)
class TiiCrossSignal(Signal):
    type: SignalType = SignalType.TIICross
    major_period: Parameter = StaticParameter(60.0)
    minor_period: Parameter = StaticParameter(30.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
