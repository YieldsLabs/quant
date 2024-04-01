from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class MacdCrossSignal(Signal):
    type: SignalType = SignalType.MacdCross
    smooth_type: Parameter = StaticParameter(Smooth.ZLEMA)
    fast_period: Parameter = StaticParameter(12.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
