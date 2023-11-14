from dataclasses import dataclass

from strategy.regime.base import BaseRegime, FilterType


@dataclass(frozen=True)
class FibFilter(BaseRegime):
    type: FilterType = FilterType.Fib
