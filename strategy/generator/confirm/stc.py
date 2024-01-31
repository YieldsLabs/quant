from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class StcConfirm(Confirm):
    type: Confirm = ConfirmType.Stc
    fast_period: Parameter = StaticParameter(25.0)
    slow_period: Parameter = StaticParameter(50.0)
    cycle: Parameter = StaticParameter(10.0)
    d_first: Parameter = StaticParameter(3.0)
    d_second: Parameter = StaticParameter(3.0)
