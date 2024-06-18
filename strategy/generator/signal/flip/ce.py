from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import SmoothATR
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CeFlipSignal(Signal):
    type: SignalType = SignalType.CeFlip
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(22.0)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(22.0)
    factor: Parameter = StaticParameter(1.8)
