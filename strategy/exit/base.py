from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple

from core.models.indicator import Indicator


class ExitType(Enum):
    Dumb = "Dumb"


@dataclass(frozen=True)
class BaseExit(Indicator):
    type: ExitType

    def parameters(self) -> Tuple[Any, ...]:
        return []
