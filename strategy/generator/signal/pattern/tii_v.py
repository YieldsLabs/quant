from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TiiVSignal(Signal):
    type: SignalType = SignalType.TiiV
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    major_period: Parameter = StaticParameter(8.0)
    minor_period: Parameter = StaticParameter(2.0)
