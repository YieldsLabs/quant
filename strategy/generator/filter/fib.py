from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Filter, FilterType


@dataclass(frozen=True)
class FibFilter(Filter):
    type: FilterType = FilterType.Fib
    period: Parameter = StaticParameter(13.0)
