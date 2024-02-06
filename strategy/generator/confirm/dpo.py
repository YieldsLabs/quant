from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class DpoConfirm(Confirm):
    type: Confirm = ConfirmType.Dpo
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(18.0)
