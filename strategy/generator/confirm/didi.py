from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class DidiConfirm(Confirm):
    type: Confirm = ConfirmType.Didi
    source: Parameter = CategoricalParameter(SourceType)
    smooth: Parameter = StaticParameter(Smooth.SMA)
    period_medium: Parameter = StaticParameter(8.0)
    period_slow: Parameter = StaticParameter(40.0)
    smooth_signal: Parameter = StaticParameter(Smooth.EMA)
    period_signal: Parameter = StaticParameter(3.0)
