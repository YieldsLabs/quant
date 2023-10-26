from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class TIIFilter(BaseFilter):
    type: FilterType = FilterType.Tii
    major_period: Parameter = RandomParameter(55.0, 65.0, 5.0)
    minor_period: Parameter = RandomParameter(25.0, 40.0, 5.0)
    threshold: Parameter = RandomParameter(0.0, 5.0, 1.0)
