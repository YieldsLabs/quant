from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ConfirmType(Enum):
    Dumb = "Dumb"
    Dpo = "Dpo"
    Dso = "Dso"
    Cci = "Cci"
    Eom = "Eom"
    Roc = "Roc"
    RsiSignalLine = "RsiSignalLine"
    RsiNeutrality = "RsiNeutrality"
    Stc = "Stc"
    Vi = "Vi"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Confirm(Indicator):
    type: ConfirmType
