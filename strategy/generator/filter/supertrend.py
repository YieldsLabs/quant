from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)

from .base import Filter, FilterType


@dataclass(frozen=True)
class SupertrendFilter(Filter):
    type: FilterType = FilterType.Supertrend
    atr_period: Parameter = StaticParameter(17.0)
    factor: Parameter = StaticParameter(5.1)
