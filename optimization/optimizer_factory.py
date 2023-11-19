from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.optimizer import Optimizer
from optimization.strategy_genetic import GeneticStrategyOptimization


class StrategyOptimizerFactory(AbstractStrategyOptimizerFactory):
    _optimizer_type = {Optimizer.GENETIC: GeneticStrategyOptimization}

    def __init__(
        self,
        max_generations: int,
        elite_count: int,
        crossover_rate: float,
        mutation_rate: float,
        tournament_size: int,
        reset_percentage: float,
        stability_percentage: float,
    ):
        super().__init__()
        self.max_generations = max_generations
        self.elite_count = elite_count
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.reset_percentage = reset_percentage
        self.stability_percentage = stability_percentage

    def create(
        self, type: Optimizer, generator: AbstractStrategyGenerator
    ) -> AbstractStrategyOptimization:
        if type not in self._optimizer_type:
            raise ValueError(f"Unknown Optimizer: {type}")

        optimizer = self._optimizer_type.get(type)

        return optimizer(
            generator,
            self.max_generations,
            self.elite_count,
            self.crossover_rate,
            self.mutation_rate,
            self.tournament_size,
            self.reset_percentage,
            self.stability_percentage,
        )
