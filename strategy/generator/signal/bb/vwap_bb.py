from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class VwapBbSignal(Signal):
    type: SignalType = SignalType.VwapBb
    period: Parameter = StaticParameter(100.0)
    bb_smooth: Parameter = StaticParameter(Smooth.SMA)
    bb_period: Parameter = StaticParameter(50.0)
    factor: Parameter = StaticParameter(2.0)
