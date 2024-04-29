from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class DsoConfirm(Confirm):
    type: Confirm = ConfirmType.Dso
    source_type: Parameter = StaticParameter(SourceType.CLOSE)
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    smooth_period: Parameter = StaticParameter(10.0)
    k_period: Parameter = StaticParameter(5.0)
    d_period: Parameter = StaticParameter(7.0)
