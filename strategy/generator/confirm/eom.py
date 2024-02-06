from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class EomConfirm(Confirm):
    type: ConfirmType = ConfirmType.Eom
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(14.0)
    divisor: Parameter = StaticParameter(10000.0)
