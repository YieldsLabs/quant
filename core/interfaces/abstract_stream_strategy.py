from abc import ABC, abstractmethod
from typing import Any

from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

class AbstractStreamStrategy(ABC):
    @abstractmethod
    async def subscribe(self):
        pass

    @abstractmethod
    async def unsubscribe(self):
        pass

    @abstractmethod
    def receive(self) -> Any:
        pass