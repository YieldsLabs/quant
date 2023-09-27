from abc import ABC, abstractmethod
from dataclasses import dataclass

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
    min: float
    max: float
    step: float = 5.0

    def __post_init__(self):
        object.__setattr__(self, "_value", self._generate_value())

    @property
    def value(self) -> float:
        return self._value

    def _generate_value(self) -> float:
        value = float(
            np.random.choice(list(np.arange(self.min, self.max + self.step, self.step)))
        )
        return round(value, 2)


@dataclass(frozen=True)
class StaticParameter(Parameter):
    _value: float

    @property
    def value(self) -> float:
        return self._value
