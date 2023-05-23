from abc import abstractmethod
from typing import List
from core.abstract_event_manager import AbstractEventManager
from core.events.portfolio import PortfolioPerformance
from core.position import Position


class AbstractAnalytics(AbstractEventManager):
    @abstractmethod
    def calculate(self, positions: List[Position]) -> PortfolioPerformance:
        pass
