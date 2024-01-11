from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class DpoConfirm(Confirm):
    type: Confirm = ConfirmType.Dpo
    period: Parameter = StaticParameter(18.0)
