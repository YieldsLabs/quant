from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import SmoothATR
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SupertrendFlipSignal(Signal):
    type: SignalType = SignalType.SupFlip
    source_type: Parameter = StaticParameter(SourceType.HL2)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(8.0)
    factor: Parameter = StaticParameter(0.89)
