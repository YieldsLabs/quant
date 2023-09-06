from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple


class MovingAverageType(Enum):
    SMA = 1
    EMA = 2
    WMA = 3
    ZLEMA = 4
    HMA = 5
    VWMA = 6
    DEMA = 7
    TEMA = 8

    def __str__(self):
        return self.name.upper()


@dataclass(frozen=True)
class Indicator:
    type: Any


@dataclass(frozen=True)
class CrossMovingAverageIndicator(Indicator):
    type: MovingAverageType
    short_period: int
    long_period: int

    @property
    def parameters(self):
        return [self.short_period, self.long_period]
