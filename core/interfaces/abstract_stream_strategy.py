from abc import ABC, abstractmethod
from typing import Any

from core.interfaces.abstract_exchange import AbstractWSExchange


class AbstractStreamStrategy(ABC):
    @abstractmethod
    async def subscribe(self, ws: AbstractWSExchange):
        pass

    @abstractmethod
    async def unsubscribe(self, ws: AbstractWSExchange):
        pass

    @abstractmethod
    def parse(self, ws: AbstractWSExchange, topic: str, message: Any) -> Any:
        pass
