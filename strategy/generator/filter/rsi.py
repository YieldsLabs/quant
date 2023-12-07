from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, RandomParameter
from core.models.rsi import RSIType

from .base import Filter, FilterType


@dataclass(frozen=True)
class RsiFilter(Filter):
    type: FilterType = FilterType.Rsi
    rsi_type: Parameter = CategoricalParameter(RSIType)
    period: Parameter = RandomParameter(30.0, 50.0, 1.0)
    threshold: Parameter = RandomParameter(2.0, 5.0, 1.0)
