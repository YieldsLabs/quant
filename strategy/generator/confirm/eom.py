from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class EomConfirm(Confirm):
    type: ConfirmType = ConfirmType.Eom
    period: Parameter = StaticParameter(14.0)
    divisor: Parameter = StaticParameter(10000.0)
