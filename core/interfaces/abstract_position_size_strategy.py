from abc import abstractmethod
from typing import Optional

from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.signal import Signal


class AbstractPositionSizeStrategy(AbstractEventManager):
    @abstractmethod
    def calculate(
        self,
        signal: Signal,
        entry_price: float,
        stop_loss_price: Optional[float] = None,
    ) -> float:
        pass
