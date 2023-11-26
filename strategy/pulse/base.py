from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class PulseType(Enum):
    Adx = "Adx"
    Dumb = "Dumb"
    Chop = "Chop"
    Osc = "Osc"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Pulse(Indicator):
    type: PulseType
