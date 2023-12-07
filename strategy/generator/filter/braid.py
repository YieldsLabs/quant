from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Filter, FilterType


@dataclass(frozen=True)
class BraidFilter(Filter):
    type: FilterType = FilterType.Braid
    period_one: Parameter = StaticParameter(3.0)
    period_two: Parameter = StaticParameter(7.0)
    period_three: Parameter = StaticParameter(14.0)
    strength: Parameter = StaticParameter(40.0)
    atr_period: Parameter = StaticParameter(14.0)
