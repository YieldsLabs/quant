from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth, SmoothATR
from core.models.source import SourceType

from .base import Pulse, PulseType


@dataclass(frozen=True)
class SqzPulse(Pulse):
    type: PulseType = PulseType.Sqz
    source: Parameter = CategoricalParameter(SourceType)
    smooth: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(20.0)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(20.0)
    factor_bb: Parameter = StaticParameter(2.0)
    factor_kch: Parameter = StaticParameter(1.2)
