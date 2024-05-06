from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CeFlipSignal(Signal):
    type: SignalType = SignalType.CeFlip
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(15.0)
    atr_period: Parameter = StaticParameter(15.0)
    factor: Parameter = StaticParameter(3.0)
