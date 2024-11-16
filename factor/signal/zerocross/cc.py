from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CcZeroCrossSignal(Signal):
    type: SignalType = SignalType.CcZeroCross
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    fast_period: Parameter = StaticParameter(11.0)
    slow_period: Parameter = StaticParameter(14.0)
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    smooth_period: Parameter = StaticParameter(20.0)
