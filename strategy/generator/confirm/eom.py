from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from core.models.source import SourceType

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class EomConfirm(Confirm):
    type: ConfirmType = ConfirmType.Eom
    source_type: Parameter = StaticParameter(SourceType.HL2)
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(16.0)
