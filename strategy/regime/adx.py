from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class ADXFilter(BaseRegime):
    type: FilterType = FilterType.Adx
    adx_period: Parameter = RandomParameter(10.0, 15.0, 2.0)
    di_period: Parameter = RandomParameter(10.0, 15.0, 2.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
