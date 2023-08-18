from abc import abstractmethod

from .abstract_actor import AbsctractActor


class AbsctractStrategyActorFactory:
    @abstractmethod
    def create_actor(self, wasm_path: str, strategy: str, paremeters: tuple[int]) -> AbsctractActor:
        pass
