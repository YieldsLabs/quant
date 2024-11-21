from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class VwapCrossSignal(Signal):
    type: SignalType = SignalType.VwapCross
    source_type: Parameter = StaticParameter(SourceType.HLC3)
    period: Parameter = StaticParameter(100.0)
