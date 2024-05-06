from abc import ABC, abstractmethod

from core.models.position import Position
from core.models.signal import Signal


class AbstractPositionFactory(ABC):
    @abstractmethod
    def create(
        self,
        signal: Signal,
    ) -> Position:
        pass
