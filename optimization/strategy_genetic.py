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
    SIGNAL = auto()
    REGIME = auto()
    VOLUME = auto()
    STOP_LOSS = auto()
    EXIT = auto()


class GeneticStrategyOptimization(AbstractStrategyOptimization):
    def __init__(
        self,
        strategy_generator: AbstractStrategyGenerator,
        max_generations: int,
        elite_count: int,
        mutation_rate: float,
        tournament_size: int,
    ):
        super().__init__()
        self.max_generations = max_generations
        self.elite_count = elite_count
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
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
        elite = sorted_population[: self.elite_count]
        parents = self._tournament_selection(sorted_population[self.elite_count :])
        return elite, parents

    def _tournament_selection(self, candidates: list[Individual]) -> list[Individual]:
        parents = []

        while len(parents) < len(candidates):
            contenders = np.random.choice(
                candidates, size=self.tournament_size, replace=True
            )
            winner = max(contenders, key=lambda individual: individual.fitness)
            parents.append(winner)

        return parents

    async def _mutate_parents(self, parents: list[Individual]) -> None:
        for idx, parent in enumerate(parents):
            if np.random.rand() < self.mutation_rate:
                parents[idx] = await self._mutate(parent)

    def _crossover_parents(self, parents: list[Individual]) -> list[Individual]:
        children = [
            self._crossover(parents[i], parents[i + 1])
            for i in range(0, len(parents) - 1, 2)
        ]
        return [child for pair in children for child in pair]

    def _update_population(
        self, elite: list[Individual], children: list[Individual]
    ) -> None:
        self._population = elite + children

    def _crossover(self, parent1, parent2):
        chosen_attr = np.random.choice(list(GeneticAttributes))

        if chosen_attr in [
            GeneticAttributes.SIGNAL,
            GeneticAttributes.REGIME,
            GeneticAttributes.VOLUME,
            GeneticAttributes.STOP_LOSS,
            GeneticAttributes.EXIT,
        ]:
            child1_strategy = Strategy(
                parent1.strategy.type,
                parent2.strategy.entry_signal
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent1.strategy.entry_signal,
                parent1.strategy.regime_filter
                if chosen_attr == GeneticAttributes.REGIME
                else parent2.strategy.regime_filter,
                parent1.strategy.volume_filter
                if chosen_attr == GeneticAttributes.VOLUME
                else parent2.strategy.volume_filter,
                parent1.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent2.strategy.stop_loss,
                parent1.strategy.exit_signal
                if chosen_attr == GeneticAttributes.EXIT
                else parent2.strategy.exit_signal,
            )
            child2_strategy = Strategy(
                parent2.strategy.type,
                parent1.strategy.entry_signal
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent2.strategy.entry_signal,
                parent2.strategy.regime_filter
                if chosen_attr == GeneticAttributes.REGIME
                else parent1.strategy.regime_filter,
                parent2.strategy.volume_filter
                if chosen_attr == GeneticAttributes.VOLUME
                else parent1.strategy.volume_filter,
                parent2.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent1.strategy.stop_loss,
                parent2.strategy.exit_signal
                if chosen_attr == GeneticAttributes.EXIT
                else parent1.strategy.exit_signal,
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
            GeneticAttributes.REGIME,
            GeneticAttributes.VOLUME,
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
