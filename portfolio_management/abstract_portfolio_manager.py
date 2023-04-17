from abc import abstractmethod
from typing import List
from core.abstract_event_manager import AbstractEventManager
from core.events.order import Order


class AbstractPortfolioManager(AbstractEventManager):
    @abstractmethod
    def calculate_performance(self, orders: List[Order]):
        pass
