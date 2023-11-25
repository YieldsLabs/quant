from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SNATRSignal(Signal):
    type: SignalType = SignalType.SnAtr
    atr_period: Parameter = StaticParameter(60.0)
    atr_smoothing_period: Parameter = StaticParameter(13.0)
    threshold: Parameter = RandomParameter(0.0, 0.2, 0.1)
