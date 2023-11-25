from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.filter.base import Filter, FilterType


@dataclass(frozen=True)
class SupertrendFilter(Filter):
    type: FilterType = FilterType.Supertrend
    atr_period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(3.0)
