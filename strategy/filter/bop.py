from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from strategy.filter.base import Filter, FilterType


@dataclass(frozen=True)
class BopFilter(Filter):
    type: FilterType = FilterType.Bop
    signal_smoothing: Parameter = StaticParameter(14.0)
