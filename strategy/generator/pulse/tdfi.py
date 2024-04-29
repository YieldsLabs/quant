from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Pulse, PulseType


@dataclass(frozen=True)
class TdfiPulse(Pulse):
    type: PulseType = PulseType.Tdfi
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = StaticParameter(14.0)
    n: Parameter = StaticParameter(3.0)
