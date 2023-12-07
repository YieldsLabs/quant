from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.optimizer import Optimizer

from ._genetic import GeneticStrategyOptimization


class StrategyOptimizerFactory(AbstractStrategyOptimizerFactory):
    _type = {Optimizer.GENETIC: GeneticStrategyOptimization}

    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config_service = config_service

    def create(
        self, type: Optimizer, generator: AbstractStrategyGenerator
    ) -> AbstractStrategyOptimization:
        if type not in self._type:
            raise ValueError(f"Unknown Optimizer: {type}")

        optimizer = self._type.get(type)

        return optimizer(
            generator,
            self.config_service,
        )
