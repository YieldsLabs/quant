from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class BOPFilter(BaseRegime):
    type: FilterType = FilterType.Bop
    signal_smoothing: Parameter = StaticParameter(14.0)
