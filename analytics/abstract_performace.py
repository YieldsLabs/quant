from abc import ABC, abstractmethod
from typing import List

from shared.order import Order


class AbstractPerformance(ABC):
    @abstractmethod
    def calculate(self, orders: List[Order]):
        raise NotImplementedError
