from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class DumbConfirm(Confirm):
    type: ConfirmType = ConfirmType.Dumb
    period: Parameter = StaticParameter(10.0)
