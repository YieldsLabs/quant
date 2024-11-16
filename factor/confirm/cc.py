from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class CcConfirm(Confirm):
    type: Confirm = ConfirmType.Cc
    source: Parameter = StaticParameter(SourceType.CLOSE)
    period_fast: Parameter = StaticParameter(14.0)
    period_slow: Parameter = StaticParameter(28.0)
    smooth: Parameter = StaticParameter(Smooth.WMA)
    period_smooth: Parameter = StaticParameter(14.0)
    smooth_signal: Parameter = StaticParameter(Smooth.SMA)
    period_signal: Parameter = StaticParameter(14.0)
