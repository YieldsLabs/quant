from abc import ABC, abstractmethod

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.optimizer import Optimizer


class AbstractStrategyOptimizerFactory(ABC):
    @abstractmethod
    def create(
        self, type: Optimizer, generator: AbstractStrategyGenerator
    ) -> AbstractStrategyOptimization:
        pass
