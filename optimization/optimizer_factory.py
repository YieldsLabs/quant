from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_optimizer_factory import AbstractStrategyOptimizerFactory
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.optimizer import Optimizer
from optimization.strategy_genetic import GeneticStrategyOptimization


class StrategyOptimizerFactory(AbstractStrategyOptimizerFactory):
    _optimizer_type = {Optimizer.GENETIC: GeneticStrategyOptimization}

    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("optimizer")

    def create(
        self, type: Optimizer, generator: AbstractStrategyGenerator
    ) -> AbstractStrategyOptimization:
        if type not in self._optimizer_type:
            raise ValueError(f"Unknown Optimizer: {type}")

        optimizer = self._optimizer_type.get(type)

        return optimizer(
            generator,
            self.config["max_generations"],
            self.config["elite_count"],
            self.config["crossover_rate"],
            self.config["mutation_rate"],
            self.config["tournament_size"],
            self.config["reset_percentage"],
            self.config["stability_percentage"],
        )
