from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter

from .base import Filter, FilterType


@dataclass(frozen=True)
class ApoFilter(Filter):
    type: FilterType = FilterType.Apo
    short_period: Parameter = StaticParameter(10.0)
    long_period: Parameter = StaticParameter(20.0)
