from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class FibFilter(BaseRegime):
    type: FilterType = FilterType.Fib
    period: Parameter = StaticParameter(13.0)
