from dataclasses import dataclass

from core.models.indicator import Indicator


@dataclass(frozen=True)
class DumbExit(Indicator):
    pass
