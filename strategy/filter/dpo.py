from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from strategy.filter.base import Filter, FilterType


@dataclass(frozen=True)
class DPOFilter(Filter):
    type: FilterType = FilterType.Dpo
    period: Parameter = StaticParameter(21.0)
