from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class CciConfirm(Confirm):
    type: Confirm = ConfirmType.Cci
    source_type: Parameter = StaticParameter(SourceType.HLC3)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(100.0)
    factor: Parameter = StaticParameter(0.015)
