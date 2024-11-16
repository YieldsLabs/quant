from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class RsiNtSignal(Signal):
    type: SignalType = SignalType.RsiNt
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.SMMA)
    period: Parameter = StaticParameter(8.0)
    threshold: Parameter = RandomParameter(0.0, 1.0, 1.0)
