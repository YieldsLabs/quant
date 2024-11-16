from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class WprConfirm(Confirm):
    type: Confirm = ConfirmType.Wpr
    source: Parameter = StaticParameter(SourceType.CLOSE)
    period: Parameter = StaticParameter(28.0)
    smooth_signal: Parameter = StaticParameter(Smooth.SMA)
    period_signal: Parameter = StaticParameter(14.0)
