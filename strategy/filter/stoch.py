from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, RandomParameter
from core.models.stoch import StochType
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class StochFilter(BaseFilter):
    type: FilterType = FilterType.Stoch
    stoch_type: Parameter = CategoricalParameter(StochType)
    period: Parameter = RandomParameter(13.0, 16.0, 1.0)
    k_period: Parameter = RandomParameter(1.0, 5.0, 1.0)
    d_period: Parameter = RandomParameter(3.0, 5.0, 1.0)
