from abc import abstractmethod
from typing import List

from .abstract_event_manager import AbstractEventManager


class AbstractPortfolioManager(AbstractEventManager):
    @abstractmethod
    def initialize_account(self):
        pass

    @abstractmethod
    def get_top_strategies(n: int) -> List[str]:
        pass
