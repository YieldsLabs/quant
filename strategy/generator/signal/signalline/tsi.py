from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TsiSignalLineSignal(Signal):
    type: SignalType = SignalType.TsiSignalLine
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    fast_period: Parameter = StaticParameter(13.0)
    slow_period: Parameter = StaticParameter(25.0)
    signal_period: Parameter = StaticParameter(13.0)
