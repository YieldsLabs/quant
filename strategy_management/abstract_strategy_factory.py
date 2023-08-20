from abc import abstractmethod

from core.timeframe import Timeframe

from .abstract_actor import AbstractActor


class AbstractStrategyActorFactory:
    @abstractmethod
    def create_actor(self, symbol: str, timeframe: Timeframe, wasm_path: str, strategy: str, paremeters: tuple[int]) -> AbstractActor:
        pass
