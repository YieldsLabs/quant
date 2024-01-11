from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class ConfirmType(Enum):
    Dumb = "Dumb"
    Dpo = "Dpo"
    Eom = "Eom"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Confirm(Indicator):
    type: ConfirmType
