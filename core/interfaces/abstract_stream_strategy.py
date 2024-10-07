from abc import ABC, abstractmethod
from typing import Any

from core.interfaces.abstract_ws import AbstractWS


class AbstractStreamStrategy(ABC):
    @abstractmethod
    async def subscribe(self, ws: AbstractWS):
        pass

    @abstractmethod
    async def unsubscribe(self, ws: AbstractWS):
        pass

    @abstractmethod
    def parse(self, message: Any) -> Any:
        pass
