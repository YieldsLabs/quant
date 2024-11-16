from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Pulse, PulseType


@dataclass(frozen=True)
class TdfiPulse(Pulse):
    type: PulseType = PulseType.Tdfi
    source: Parameter = StaticParameter(SourceType.CLOSE)
    smooth: Parameter = CategoricalParameter(Smooth)
    period: Parameter = StaticParameter(8.0)
    n: Parameter = StaticParameter(3.0)
