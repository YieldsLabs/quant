from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class MacdBbSignal(Signal):
    type: SignalType = SignalType.MacdBb
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    fast_period: Parameter = StaticParameter(8.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
    bb_period: Parameter = StaticParameter(9.0)
    factor: Parameter = StaticParameter(0.8)
