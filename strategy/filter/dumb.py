from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.filter.base import Filter, FilterType


@dataclass(frozen=True)
class DumbFilter(Filter):
    type: FilterType = FilterType.Dumb
    period: Parameter = StaticParameter(10.0)
