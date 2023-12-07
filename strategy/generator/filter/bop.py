from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Filter, FilterType


@dataclass(frozen=True)
class BopFilter(Filter):
    type: FilterType = FilterType.Bop
    signal_smoothing: Parameter = StaticParameter(14.0)
