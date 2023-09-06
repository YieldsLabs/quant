from dataclasses import dataclass
from enum import Enum
from typing import Any
import numpy as np


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
class Parameter:
    min: int
    max: int
    step: int = 5

    def __post_init__(self):
        object.__setattr__(self, "_value", self._generate_value())

    @property
    def value(self) -> int:
        return self._value

    def _generate_value(self) -> int:
        return int(np.random.choice([x for x in np.arange(self.min, self.max + self.step, self.step)]))

@dataclass(frozen=True)
class Indicator:
    type: Any


@dataclass(frozen=True)
class CrossMovingAverageIndicator(Indicator):
    type: MovingAverageType
    short_period: Parameter = Parameter(5, 50, 5)
    long_period: Parameter = Parameter(50, 200, 10)

    @property
    def parameters(self):
        return (self.short_period.value, self.long_period.value,)
