from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Indicator(ABC):
    type: Any
