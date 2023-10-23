from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class MovingAverageFilter(BaseFilter):
    type: FilterType = FilterType.Ma
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = StaticParameter(200.0)
