from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DiSignalLineSignal(Signal):
    type: SignalType = SignalType.DiSignalLine
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    signal_period: Parameter = RandomParameter(4.0, 8.0, 1.0)
