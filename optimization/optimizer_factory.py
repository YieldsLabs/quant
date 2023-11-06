from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.optimizer import Optimizer
from optimization.strategy_genetic import GeneticStrategyOptimization


class StrategyOptimizerFactory(AbstractStrategyOptimizerFactory):
    _optimizer_type = {Optimizer.GENETIC: GeneticStrategyOptimization}

    def __init__(self, max_generations: int, elite_count: int, mutation_rate: float):
        super().__init__()
        self.max_generations = max_generations
        self.elite_count = elite_count
        self.mutation_rate = mutation_rate

    def create(
        self, type: Optimizer, generator: AbstractStrategyGenerator
    ) -> AbstractStrategyOptimization:
        if type not in self._optimizer_type:
            raise ValueError(f"Unknown Optimizer: {type}")

        optimizer = self._optimizer_type.get(type)

        return optimizer(
            generator, self.max_generations, self.elite_count, self.mutation_rate
        )
