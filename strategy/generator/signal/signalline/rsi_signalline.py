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
class RsiSignalLineSignal(Signal):
    type: SignalType = SignalType.RsiSignalLine
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    rsi_period: Parameter = RandomParameter(12.0, 15.0, 1.0)
    smooth_signal: Parameter = StaticParameter(Smooth.EMA)
    smooth_period: Parameter = RandomParameter(7.0, 10.0, 1.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
