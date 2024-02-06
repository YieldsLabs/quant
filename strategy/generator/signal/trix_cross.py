from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class TrixCrossSignal(Signal):
    type: SignalType = SignalType.TrixCross
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(7.0)
    signal_period: Parameter = StaticParameter(9.0)
