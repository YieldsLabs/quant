from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import SmoothATR
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SupertrendFlipSignal(Signal):
    type: SignalType = SignalType.SupFlip
    source_type: Parameter = StaticParameter(SourceType.HL2)
    smooth_atr: Parameter = StaticParameter(SmoothATR.SMMA)
    period_atr: Parameter = StaticParameter(8.0)
    factor: Parameter = StaticParameter(0.86)
