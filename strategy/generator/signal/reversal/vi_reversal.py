from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class ViReversalSignal(Signal):
    type: SignalType = SignalType.ViReversal
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(4.0)
