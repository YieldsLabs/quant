from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from core.models.source import SourceType
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SpreadSignal(Signal):
    type: SignalType = SignalType.Spread
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = StaticParameter(Smooth.EMA)
    period_fast: Parameter = StaticParameter(6.0)
    period_slow: Parameter = StaticParameter(8.0)
