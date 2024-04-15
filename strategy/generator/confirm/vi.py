from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.generator.confirm.base import Confirm, ConfirmType


@dataclass(frozen=True)
class ViConfirm(Confirm):
    type: ConfirmType = ConfirmType.Vi
    atr_period: Parameter = StaticParameter(1.0)
    period: Parameter = StaticParameter(14.0)
