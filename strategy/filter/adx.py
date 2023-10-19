from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class ADXFilter(BaseFilter):
    type: FilterType = FilterType.Adx
    adx_period: Parameter = RandomParameter(10.0, 15.0, 1.0)
    di_period: Parameter = RandomParameter(10.0, 15.0, 1.0)
    threshold: Parameter = RandomParameter(25.0, 100.0, 5.0)
