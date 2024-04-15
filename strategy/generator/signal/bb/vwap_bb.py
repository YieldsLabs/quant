from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class VwapBbSignal(Signal):
    type: SignalType = SignalType.VwapBb
    period: Parameter = StaticParameter(100.0)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    bb_period: Parameter = StaticParameter(50.0)
    factor: Parameter = StaticParameter(2.0)
