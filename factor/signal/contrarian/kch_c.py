from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth, SmoothATR
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class KchCSignal(Signal):
    type: SignalType = SignalType.KchC
    source: Parameter = StaticParameter(SourceType.HLC3)
    smooth: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(20.0)
    smooth_atr: Parameter = StaticParameter(SmoothATR.SMMA)
    period_atr: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(1.0)
