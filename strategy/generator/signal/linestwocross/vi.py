from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class ViDmiLines2CrossSignal(Signal):
    type: SignalType = SignalType.ViLines2Cross
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(14.0)
