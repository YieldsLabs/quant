from abc import ABC, abstractmethod


class AbstractStrategyGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass