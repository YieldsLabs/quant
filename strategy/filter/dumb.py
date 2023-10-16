from dataclasses import dataclass

from strategy.filter.base import BaseFilter, FilterType


@dataclass(frozen=True)
class DumbFilter(BaseFilter):
    type: FilterType
