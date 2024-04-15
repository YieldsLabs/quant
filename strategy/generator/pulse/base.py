from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class PulseType(Enum):
    Adx = "Adx"
    Braid = "Braid"
    Dumb = "Dumb"
    Chop = "Chop"
    Nvol = "Nvol"
    Vo = "Vo"
    Tdfi = "Tdfi"
    Wae = "Wae"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Pulse(Indicator):
    type: PulseType
