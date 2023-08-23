from abc import abstractmethod
from typing import Any, List

from .abstract_event_manager import AbstractEventManager

from ..models.strategy import Strategy

class AbstractPortfolioManager(AbstractEventManager):
    @abstractmethod
    def initialize_account(self):
        pass

    @abstractmethod
    def get_top_strategies(n: int) -> List[Strategy]:
        pass
