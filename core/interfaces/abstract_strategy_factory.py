from abc import abstractmethod

from .abstract_actor import AbstractActor

from ..models.timeframe import Timeframe


class AbstractStrategyActorFactory:
    @abstractmethod
    def create_actor(self, symbol: str, timeframe: Timeframe, wasm_path: str, strategy: str, paremeters: tuple[int]) -> AbstractActor:
        pass
