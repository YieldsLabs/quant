from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from strategy.filter.base import FilterType
from strategy.signal.base import BaseSignal


@dataclass(frozen=True)
class RibbonFilter(BaseSignal):
    type: FilterType = FilterType.Ribbon
    smoothing: Parameter = CategoricalParameter(MovingAverageType)
    first_period: Parameter = StaticParameter(20.0)
    second_period: Parameter = StaticParameter(50.0)
    third_period: Parameter = StaticParameter(100.0)
    fourth_period: Parameter = StaticParameter(200.0)
