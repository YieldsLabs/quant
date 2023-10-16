from dataclasses import dataclass

from core.models.moving_average import MovingAverageType
from core.models.parameter import Parameter, RandomParameter
from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class MovingAverageFilter(BaseFilter):
    type: FilterType = FilterType.MA
    smoothing: MovingAverageType = MovingAverageType.EMA
    period: Parameter = RandomParameter(100.0, 300.0, 10.0)

    @property
    def parameters(self):
        return [self.smoothing, self.period]
