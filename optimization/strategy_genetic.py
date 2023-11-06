from enum import Enum, auto

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_optimization import AbstractStrategyOptimization
from core.models.individual import Individual
from core.models.strategy import Strategy
from core.queries.portfolio import GetFitness


class GeneticAttributes(Enum):
    SYMBOL = auto()
    TIMEFRAME = auto()
    STRATEGY = auto()


class GeneticStrategyOptimization(AbstractStrategyOptimization):
    def __init__(
        self,
        strategy_generator: AbstractStrategyGenerator,
        max_generations: int,
        elite_count: int,
        mutation_rate: float,
    ):
        super().__init__()
        self.max_generations = max_generations
        self.elite_count = elite_count
        self.mutation_rate = mutation_rate
        self.strategy_generator = strategy_generator
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
        return self.generation >= self.max_generations - 1

    def init(self):
        self._population = []
        self.generation = 0

        data = self.strategy_generator.generate()

        for symbol, timeframe, strategy in data:
            self._population.append(Individual(symbol, timeframe, strategy))

    async def optimize(self):
        for individual in self._population:
            fitness_value = await self.query(
                GetFitness(individual.symbol, individual.timeframe, individual.strategy)
            )
            individual.update_fitness(fitness_value)

        elite = sorted(
            self._population, key=lambda individual: individual.fitness, reverse=True
        )[: self.elite_count]

        candidates = list(self._population)
        parents = []

        while len(parents) < (len(self._population) - self.elite_count):
            contenders = np.random.choice(candidates, size=5, replace=True)
            winner = max(contenders, key=lambda individual: individual.fitness)
            parents.append(winner)
            candidates.remove(winner)

        if len(parents) % 2 != 0:
            parents.pop()

        for idx, parent in enumerate(parents):
            if np.random.rand() < self.mutation_rate:
                parents[idx] = await self._mutate(parent)

        children = []

        for i in range(0, len(parents), 2):
            child1, child2 = self._crossover(parents[i], parents[i + 1])
            children.extend([child1, child2])

        self._population[: len(children)] = children
        self._population[: self.elite_count] = elite

        self.generation += 1

    def _crossover(self, parent1, parent2):
        chosen_attr = np.random.choice(list(GeneticAttributes))

        if parent1.strategy.type == parent2.strategy.type:
            if chosen_attr == GeneticAttributes.STRATEGY:
                child1_strategy = Strategy(
                    parent1.strategy.type,
                    parent2.strategy.entry_signal,
                    parent1.strategy.regime_filter,
                    parent1.strategy.stop_loss,
                    parent1.strategy.exit_signal,
                )
                child2_strategy = Strategy(
                    parent2.strategy.type,
                    parent1.strategy.entry_signal,
                    parent2.strategy.regime_filter,
                    parent2.strategy.stop_loss,
                    parent2.strategy.exit_signal,
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

        if mutation_choice == GeneticAttributes.STRATEGY:
            strategies = self.strategy_generator.generate_strategies()
            individual.strategy = np.random.choice(strategies)

        elif mutation_choice == GeneticAttributes.SYMBOL:
            symbols = self.strategy_generator.generate_symbols()
            individual.symbol = np.random.choice(symbols)

        elif mutation_choice == GeneticAttributes.TIMEFRAME:
            timeframes = self.strategy_generator.generate_timeframes()
            individual.timeframe = np.random.choice(timeframes)

        return individual
