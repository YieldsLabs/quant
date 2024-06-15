from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ConfirmType(Enum):
    Braid = "Braid"
    Dumb = "Dumb"
    Dpo = "Dpo"
    Cci = "Cci"
    Eom = "Eom"
    RsiSignalLine = "RsiSignalLine"
    RsiNeutrality = "RsiNeutrality"
    Stc = "Stc"
    Wpr = "Wpr"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Confirm(Indicator):
    type: ConfirmType
