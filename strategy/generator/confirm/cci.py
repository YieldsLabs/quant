from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from strategy.generator.confirm.base import Confirm, ConfirmType


@dataclass(frozen=True)
class CciConfirm(Confirm):
    type: Confirm = ConfirmType.Cci
    smooth_type: Parameter = StaticParameter(Smooth.SMA)
    period: Parameter = StaticParameter(100.0)
    factor: Parameter = StaticParameter(0.015)
