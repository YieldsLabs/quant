from abc import abstractmethod
from typing import List

from core.abstract_event_manager import AbstractEventManager


class AbstractOptimization(AbstractEventManager):
    @abstractmethod
    def get_top_strategies(self, num: int) -> List[str]:
        pass

    @abstractmethod
    def get_all_strategies(self) -> List[str]:
        pass
