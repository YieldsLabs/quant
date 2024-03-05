from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class BraidConfirm(Confirm):
    type: ConfirmType = ConfirmType.Braid
    smooth_type: Parameter = CategoricalParameter(Smooth)
    period_one: Parameter = StaticParameter(3.0)
    period_two: Parameter = StaticParameter(7.0)
    period_three: Parameter = StaticParameter(14.0)
    strength: Parameter = StaticParameter(40.0)
    atr_period: Parameter = StaticParameter(14.0)