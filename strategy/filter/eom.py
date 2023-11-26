from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from strategy.filter.base import Filter, FilterType


@dataclass(frozen=True)
class EOMFilter(Filter):
    type: FilterType = FilterType.Eom
    period: Parameter = StaticParameter(14.0)
    divisor: Parameter = StaticParameter(10000.0)
