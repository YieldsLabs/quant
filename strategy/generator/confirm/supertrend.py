from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class SupertrendConfirm(Confirm):
    type: Confirm = ConfirmType.Sup
    atr_period: Parameter = StaticParameter(22.0)
    factor: Parameter = StaticParameter(5.0)
