from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Pulse, PulseType


@dataclass(frozen=True)
class WaePulse(Pulse):
    type: PulseType = PulseType.Wae
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = CategoricalParameter(Smooth)
    period_fast: Parameter = StaticParameter(10.0)
    period_slow: Parameter = StaticParameter(29.0)
    smooth_bb: Parameter = CategoricalParameter(Smooth)
    period_bb: Parameter = StaticParameter(13.0)
    factor: Parameter = StaticParameter(1.2)
    strength: Parameter = StaticParameter(69.0)
