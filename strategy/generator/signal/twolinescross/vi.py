from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class Vi2LinesCrossSignal(Signal):
    type: SignalType = SignalType.Vi2LinesCross
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(14.0)
