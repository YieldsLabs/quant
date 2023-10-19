from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class Parameter(ABC):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    def __lt__(self, other: "Parameter") -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return self.value < other.value


@dataclass(frozen=True)
class RandomParameter(Parameter):
    min: float = 1.0
    max: float = 10.0
    step: float = 5.0
    _value: float = field(init=False, default=None)

    def __post_init__(self):
        object.__setattr__(self, "_value", self._generate_value())

    @property
    def value(self) -> float:
        return self._value

    def _generate_value(self) -> float:
        value = round(np.random.uniform(self.min, self.max), 2)
        value = round(value / self.step) * self.step

        return round(value, 2)

    def __str__(self):
        return f"{self._value}"


@dataclass(frozen=True)
class StaticParameter(Parameter):
    _value: float

    @property
    def value(self) -> float:
        return self._value

    def __str__(self):
        return f"{self._value}"
