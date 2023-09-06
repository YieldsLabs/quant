from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Parameter:
    min: float 
    max: float
    step: float = 5.0

    def __post_init__(self):
        object.__setattr__(self, "_value", self._generate_value())

    @property
    def value(self) -> float:
        return self._value

    def _generate_value(self) -> float:
        value = float(np.random.choice([x for x in np.arange(self.min, self.max + self.step, self.step)]))
        return round(value, 2)

