from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class RocConfirm(Confirm):
    type: Confirm = ConfirmType.Roc
    period: Parameter = StaticParameter(21.0)
