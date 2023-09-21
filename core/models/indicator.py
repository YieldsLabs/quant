from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class Indicator(ABC):
    @property
    @abstractmethod
    def parameters(self) -> Tuple[Any, ...]:
        pass