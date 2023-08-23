from abc import abstractmethod
from typing import Optional

from .abstract_event_manager import AbstractEventManager
from ..models.position import Position


class AbstractPositionStorage(AbstractEventManager):
    @abstractmethod
    def total_pnl(self) -> float:
        pass

    @abstractmethod
    def get_active_position(self, symbol: str) -> Optional[Position]:
        pass
