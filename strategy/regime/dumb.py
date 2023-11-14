from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class DumbFilter(BaseRegime):
    type: FilterType = FilterType.Dumb
    period: Parameter = StaticParameter(50.0)
