from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class APOFilter(BaseRegime):
    type: FilterType = FilterType.Apo
    short_period: Parameter = StaticParameter(10.0)
    long_period: Parameter = StaticParameter(20.0)
