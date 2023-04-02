from abc import ABC, abstractmethod
from typing import List

from shared.order import Order

class AbstractScreening(ABC):
    @abstractmethod
    def run(self):
        pass