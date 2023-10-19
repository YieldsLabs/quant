from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class DumbFilter(BaseFilter):
    type: FilterType = FilterType.Dumb
    period: Parameter = StaticParameter(50.0)
