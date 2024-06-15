from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CeFlipSignal(Signal):
    type: SignalType = SignalType.CeFlip
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(22.0)
    smooth_atr: Parameter = StaticParameter(Smooth.SMMA)
    period_atr: Parameter = StaticParameter(22.0)
    factor: Parameter = StaticParameter(6.8)
