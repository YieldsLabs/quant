from abc import abstractmethod

from core.interfaces.abstract_event_manager import AbstractEventManager


class AbstractStrategyOptimization(AbstractEventManager):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def optimize(self):
        pass

    @property
    @abstractmethod
    def population(self):
        pass

    @property
    @abstractmethod
    def done(self) -> bool:
        pass
