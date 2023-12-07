from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Filter, FilterType


@dataclass(frozen=True)
class DpoFilter(Filter):
    type: FilterType = FilterType.Dpo
    period: Parameter = StaticParameter(21.0)
