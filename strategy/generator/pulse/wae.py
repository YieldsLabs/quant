from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Pulse, PulseType


@dataclass(frozen=True)
class WaePulse(Pulse):
    type: PulseType = PulseType.Wae
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    fast_period: Parameter = StaticParameter(20.0)
    slow_period: Parameter = StaticParameter(40.0)
    smooth_bb: Parameter = StaticParameter(Smooth.SMA)
    bb_period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(2.0)
    strength: Parameter = StaticParameter(150.0)
    atr_period: Parameter = StaticParameter(100.0)
    dz_factor: Parameter = StaticParameter(3.7)
