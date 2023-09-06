from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple


class StopLossType(Enum):
    ATR = 1

    def __str__(self):
        return self.name.upper()


@dataclass(frozen=True)
class StopLoss:
    type: StopLossType
    parameters: Tuple[Any, ...]