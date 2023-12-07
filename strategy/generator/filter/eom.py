from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Filter, FilterType


@dataclass(frozen=True)
class EomFilter(Filter):
    type: FilterType = FilterType.Eom
    period: Parameter = StaticParameter(14.0)
    divisor: Parameter = StaticParameter(10000.0)
