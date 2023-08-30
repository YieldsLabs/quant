from abc import ABC, abstractmethod

from .abstract_actor import AbstractActor

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractSignalActorFactory(ABC):
    @abstractmethod
    def create_actor(self, symbol: Symbol, timeframe: Timeframe, wasm_path: str, strategy: str, paremeters: tuple[int]) -> AbstractActor:
        pass
