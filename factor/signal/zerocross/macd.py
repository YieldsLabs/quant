from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MacdZeroCrossSignal(Signal):
    type: SignalType = SignalType.MacdZeroCross
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = CategoricalParameter(Smooth)
    fast_period: Parameter = StaticParameter(12.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
