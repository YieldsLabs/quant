from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class MovingAverageFilter(BaseRegime):
    type: FilterType = FilterType.Ma
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    period: Parameter = StaticParameter(200.0)
