from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class VwapBbSignal(Signal):
    type: SignalType = SignalType.VwapBb
    period: Parameter = StaticParameter(100.0)
    smooth_type: Parameter = CategoricalParameter(Smooth)
    bb_period: Parameter = StaticParameter(50.0)
    factor: Parameter = StaticParameter(2.0)
