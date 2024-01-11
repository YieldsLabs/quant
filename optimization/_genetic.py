from enum import Enum, auto

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.individual import Individual
from core.models.strategy import Strategy
from core.queries.portfolio import GetFitness


class GeneticAttributes(Enum):
    SYMBOL = auto()
    TIMEFRAME = auto()
    SIGNAL = auto()
    CONFIRM = auto()
    PULSE = auto()
    BASELINE = auto()
    STOP_LOSS = auto()
    EXIT = auto()


class GeneticStrategyOptimization(AbstractStrategyOptimization):
    def __init__(
        self,
        strategy_generator: AbstractStrategyGenerator,
        config_service: AbstractConfig,
    ):
        super().__init__()
        self.strategy_generator = strategy_generator
        self.config = config_service.get("optimization")
        self._population: list[Individual] = []
        self.generation = 0

    @property
    def population(self):
        return [
            (individual.symbol, individual.timeframe, individual.strategy)
            for individual in self._population
        ]

    @property
    def done(self):
        return self.generation >= self.config["max_generations"] - 1

    def init(self):
        self._population = []
        self.generation = 0

        data = self.strategy_generator.generate()
        self._population = [
            Individual(symbol, timeframe, strategy)
            for symbol, timeframe, strategy in data
        ]

    async def optimize(self):
        await self._evaluate_fitness()

        elite, parents = self._select_elite_and_parents()

        await self._mutate_parents(parents)

        children = self._crossover_parents(parents)
        self._update_population(elite, children)

        self.generation += 1

    async def _evaluate_fitness(self) -> None:
        for individual in self._population:
            fitness_value = await self.query(
                GetFitness(individual.symbol, individual.timeframe, individual.strategy)
            )
            individual.update_fitness(fitness_value)

    def _select_elite_and_parents(self) -> tuple[list[Individual], list[Individual]]:
        sorted_population = sorted(
            self._population, key=lambda individual: individual.fitness, reverse=True
        )
        elite = sorted_population[: self.config["elite_count"]]

        total_size = len(sorted_population)
        reset_size = int(self.config["reset_percentage"] * total_size)
        stability_size = int(self.config["stability_percentage"] * total_size)

        reset_parents = self._tournament_selection(
            sorted_population[
                self.config["elite_count"] : self.config["elite_count"] + reset_size
            ]
        )

        stability_parents = self._tournament_selection(
            sorted_population[
                self.config["elite_count"]
                + reset_size : self.config["elite_count"]
                + reset_size
                + stability_size
            ]
        )

        parents = reset_parents + stability_parents
        return elite, parents

    def _tournament_selection(self, candidates: list[Individual]) -> list[Individual]:
        parents = []

        while len(parents) < len(candidates):
            contenders = np.random.choice(
                candidates, size=self.config["tournament_size"], replace=True
            )
            winner = max(contenders, key=lambda individual: individual.fitness)
            parents.append(winner)

        return parents

    async def _mutate_parents(self, parents: list[Individual]) -> None:
        for idx, parent in enumerate(parents):
            if np.random.rand() < self.config["mutation_rate"]:
                parents[idx] = await self._mutate(parent)

    def _crossover_parents(self, parents: list[Individual]) -> list[Individual]:
        children = []

        for i in range(0, len(parents) - 1, 2):
            if np.random.rand() < self.config["crossover_rate"]:
                child1, child2 = self._crossover(parents[i], parents[i + 1])
                children.extend([child1, child2])
            else:
                children.extend([parents[i], parents[i + 1]])

        return children

    def _update_population(
        self, elite: list[Individual], children: list[Individual]
    ) -> None:
        self._population = elite + children

    def _crossover(self, parent1, parent2):
        chosen_attr = np.random.choice(list(GeneticAttributes))

        if chosen_attr in [
            GeneticAttributes.SIGNAL,
            GeneticAttributes.CONFIRM,
            GeneticAttributes.PULSE,
            GeneticAttributes.BASELINE,
            GeneticAttributes.STOP_LOSS,
            GeneticAttributes.EXIT,
        ]:
            child1_strategy = Strategy(
                parent1.strategy.type,
                parent2.strategy.entry
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent1.strategy.entry,
                parent1.strategy.confirm
                if chosen_attr == GeneticAttributes.CONFIRM
                else parent2.strategy.confirm,
                parent1.strategy.pulse
                if chosen_attr == GeneticAttributes.PULSE
                else parent2.strategy.pulse,
                parent1.strategy.baseline
                if chosen_attr == GeneticAttributes.BASELINE
                else parent2.strategy.baseline,
                parent1.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent2.strategy.stop_loss,
                parent1.strategy.exit
                if chosen_attr == GeneticAttributes.EXIT
                else parent2.strategy.exit,
            )
            child2_strategy = Strategy(
                parent2.strategy.type,
                parent1.strategy.entry
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent2.strategy.entry,
                parent2.strategy.confirm
                if chosen_attr == GeneticAttributes.CONFIRM
                else parent1.strategy.confirm,
                parent2.strategy.pulse
                if chosen_attr == GeneticAttributes.PULSE
                else parent1.strategy.pulse,
                parent2.strategy.baseline
                if chosen_attr == GeneticAttributes.BASELINE
                else parent1.strategy.baseline,
                parent2.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent1.strategy.stop_loss,
                parent2.strategy.exit
                if chosen_attr == GeneticAttributes.EXIT
                else parent1.strategy.exit,
            )

            return Individual(
                parent1.symbol, parent1.timeframe, child1_strategy
            ), Individual(parent2.symbol, parent2.timeframe, child2_strategy)

        if chosen_attr == GeneticAttributes.SYMBOL:
            return Individual(
                parent2.symbol, parent1.timeframe, parent1.strategy
            ), Individual(parent1.symbol, parent2.timeframe, parent2.strategy)

        elif chosen_attr == GeneticAttributes.TIMEFRAME:
            return Individual(
                parent1.symbol, parent2.timeframe, parent1.strategy
            ), Individual(parent2.symbol, parent1.timeframe, parent2.strategy)

        return parent1, parent2

    async def _mutate(self, individual):
        mutation_choice = np.random.choice(list(GeneticAttributes))

        if mutation_choice in [
            GeneticAttributes.SIGNAL,
            GeneticAttributes.CONFIRM,
            GeneticAttributes.PULSE,
            GeneticAttributes.BASELINE,
            GeneticAttributes.STOP_LOSS,
            GeneticAttributes.EXIT,
        ]:
            strategies = self.strategy_generator.generate_strategies()
            individual.strategy = np.random.choice(strategies)

        elif mutation_choice == GeneticAttributes.SYMBOL:
            symbols = self.strategy_generator.generate_symbols()
            individual.symbol = np.random.choice(symbols)

        elif mutation_choice == GeneticAttributes.TIMEFRAME:
            timeframes = self.strategy_generator.generate_timeframes()
            individual.timeframe = np.random.choice(timeframes)

        return individual
