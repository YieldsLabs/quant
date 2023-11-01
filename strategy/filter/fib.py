from dataclasses import dataclass

from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class FibFilter(BaseFilter):
    type: FilterType = FilterType.Fib
