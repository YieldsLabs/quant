from abc import ABC, abstractmethod
from typing import Any


class AbstractStreamStrategy(ABC):
    @abstractmethod
    async def subscribe(self):
        pass

    @abstractmethod
    async def unsubscribe(self):
        pass

    @abstractmethod
    def parse(self, message: Any) -> Any:
        pass
