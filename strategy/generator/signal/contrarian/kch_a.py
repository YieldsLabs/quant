from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth, SmoothATR
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class KchASignal(Signal):
    type: SignalType = SignalType.KchA
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.UTLS)
    period: Parameter = RandomParameter(20.0, 60.0, 10.0)
    smooth_atr: Parameter = StaticParameter(SmoothATR.UTLS)
    period_atr: Parameter = RandomParameter(20.0, 80.0, 10.0)
    factor: Parameter = RandomParameter(0.3, 2.0, 0.1)
