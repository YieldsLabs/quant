from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class CciConfirm(Confirm):
    type: Confirm = ConfirmType.Cci
    source: Parameter = StaticParameter(SourceType.HLC3)
    period: Parameter = StaticParameter(100.0)
    factor: Parameter = StaticParameter(0.015)
    smooth: Parameter = StaticParameter(Smooth.EMA)
    period_smooth: Parameter = StaticParameter(14.0)
