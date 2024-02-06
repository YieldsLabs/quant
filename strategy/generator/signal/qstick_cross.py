from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class QstickCrossSignal(Signal):
    type: SignalType = SignalType.QstickCross
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
    signal_period: Parameter = RandomParameter(4.0, 8.0, 1.0)
