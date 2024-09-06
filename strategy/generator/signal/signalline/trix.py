from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TrixSignalLineSignal(Signal):
    type: SignalType = SignalType.TrixSignalLine
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(7.0)
    signal_period: Parameter = StaticParameter(9.0)
