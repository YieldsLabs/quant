from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth, SmoothATR
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class KchASignal(Signal):
    type: SignalType = SignalType.KchA
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.UTLS)
    period: Parameter = StaticParameter(60.0)
    smooth_atr: Parameter = StaticParameter(SmoothATR.UTLS)
    period_atr: Parameter = StaticParameter(80.0)
    factor: Parameter = StaticParameter(0.56)
