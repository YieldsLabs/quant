from abc import abstractmethod

from .abstract_actor import AbstractActor


class AbsctractStrategyActorFactory:
    @abstractmethod
    def create_actor(self, wasm_path: str, strategy: str, paremeters: tuple[int]) -> AbstractActor:
        pass
