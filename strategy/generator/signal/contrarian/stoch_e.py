from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class StochESignal(Signal):
    type: SignalType = SignalType.StochE
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(34.0)
    period_k: Parameter = StaticParameter(5.0)
    period_d: Parameter = StaticParameter(3.0)
    threshold: Parameter = RandomParameter(0.0, 1.0, 1.0)
