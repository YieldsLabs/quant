from dataclasses import dataclass

from core.models.indicator import Indicator


@dataclass(frozen=True)
class DumbFilter(Indicator):
    @property
    def parameters(self):
        return []
