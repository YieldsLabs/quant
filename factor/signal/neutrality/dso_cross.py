from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DsoNeutralityCrossSignal(Signal):
    type: Signal = SignalType.DsoNeutralityCross
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    smooth_period: Parameter = StaticParameter(13.0)
    k_period: Parameter = StaticParameter(8.0)
    d_period: Parameter = StaticParameter(9.0)
