from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Pulse, PulseType


@dataclass(frozen=True)
class WaePulse(Pulse):
    type: PulseType = PulseType.Wae
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    fast_period: Parameter = StaticParameter(15.0)
    slow_period: Parameter = StaticParameter(30.0)
    smooth_bb: Parameter = StaticParameter(Smooth.SMA)
    bb_period: Parameter = StaticParameter(15.0)
    factor: Parameter = StaticParameter(2.0)
    strength: Parameter = StaticParameter(150.0)
