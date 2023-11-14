from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class VolumeType(Enum):
    Dumb = "Dumb"
    Osc = "Osc"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseVolume(Indicator):
    type: VolumeType
