from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MacdColorSwitchSignal(Signal):
    type: SignalType = SignalType.MacdColorSwitch
    source_type: Parameter = StaticParameter(SourceType.HLC3)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    fast_period: Parameter = StaticParameter(12.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
