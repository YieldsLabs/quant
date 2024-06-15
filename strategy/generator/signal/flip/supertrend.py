from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SupertrendFlipSignal(Signal):
    type: SignalType = SignalType.SupFlip
    source_type: Parameter = StaticParameter(SourceType.HL2)
    atr_period: Parameter = StaticParameter(15.0)
    factor: Parameter = StaticParameter(1.4)
