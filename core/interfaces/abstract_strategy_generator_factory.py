from abc import ABC, abstractmethod

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.symbol import Symbol


class AbstractStrategyGeneratorFactory(ABC):
    @abstractmethod
    def create(self, symbols: list[Symbol]) -> AbstractStrategyGenerator:
        pass
