from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class AoZeroCrossSignal(Signal):
    type: SignalType = SignalType.AoZeroCross
    source_type: Parameter = StaticParameter(SourceType.HL2)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    fast_period: Parameter = StaticParameter(5.0)
    slow_period: Parameter = StaticParameter(34.0)
