from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TRIXCrossSignal(Signal):
    type: SignalType = SignalType.TrixCross
    period: Parameter = StaticParameter(18.0)
    signal_period: Parameter = StaticParameter(9.0)