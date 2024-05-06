from abc import abstractmethod

from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.signal import Signal


class AbstractOrderSizeStrategy(AbstractEventManager):
    @abstractmethod
    def calculate(
        self,
        signal: Signal,
    ) -> float:
        pass
