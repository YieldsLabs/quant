from enum import Enum, auto
from typing import Tuple, Union

import numpy as np

from coral import DataSourceFactory
from core.actors import BaseActor
from core.commands.factor import EnvolveGeneration, InitGeneration
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.individual import Individual
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.broker import GetSymbols
from core.queries.factor import GetGeneration
from core.queries.portfolio import GetPortfolioPerformance

from .generator import PopulationGenerator

FactorEvent = Union[InitGeneration, GetGeneration, EnvolveGeneration]

class GeneticAttributes(Enum):
    SIGNAL = auto()
    CONFIRM = auto()
    PULSE = auto()
    BASELINE = auto()
    STOP_LOSS = auto()
    EXIT = auto()


class FactorActor(BaseActor, EventHandlerMixin):
    def __init__(self, datasource: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.datasource = datasource
        self.config = config_service.get("factor")
        self.population = []
        self.generation = 0

    async def on_receive(self, event: FactorEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(InitGeneration, self._init_generation)
        self.register_handler(GetGeneration, self._get_generation)
        self.register_handler(EnvolveGeneration, self._envolve_generation)

    async def _init_generation(self, msg: InitGeneration):
        self.population = []
        self.generation = 0

        generator = self._get_generator(msg.datasource, msg.cap)

        for individual in generator:
            self.population.append(individual)

    async def _get_generator(self, datasource, cap):
        symbols = await self.ask(GetSymbols(datasource, cap))

        timeframes = [
            Timeframe.from_raw(timeframe)
            for timeframe in self.config.get("timeframes", ["15m"])
        ]

        return PopulationGenerator(
            symbols, timeframes, self.config.get("n_samples", 2)
        )

    async def _get_generation(
        self, _msg: GetGeneration
    ) -> Tuple[list[Tuple[Symbol, Timeframe, Strategy]], float]:
        population = [(i.symbol, i.timeframe, i.strategy) for i in self.population]

        return (population, self.generation)

    async def _envolve_generation(self, msg: EnvolveGeneration):
        await self._evaluate_fitness()

        elite, parents = self._select_elite_and_parents()

        generator = self._get_generator(msg.datasource, msg.cap)

        await self._mutate_parents(parents, generator)

        children = self._crossover_parents(parents)
        self._update_population(elite, children)

        self.population = list(set(self.population))

        self.generation += 1

    async def _evaluate_fitness(self) -> None:
        for individual in self.population:
            performance = await self.ask(
                GetPortfolioPerformance(individual.symbol, individual.timeframe, individual.strategy)
            )
            
            fitness_value = performance.deflated_sharpe_ratio

            individual.update_fitness(fitness_value)

    def _update_population(
        self, elite: list[Individual], children: list[Individual]
    ) -> None:
        self.population = elite + children

    def _select_elite_and_parents(self) -> tuple[list[Individual], list[Individual]]:
        sorted_population = sorted(
            self.population, key=lambda individual: individual.fitness, reverse=True
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
    
    async def _mutate_parents(self, parents: list[Individual], generator) -> None:
        for idx, parent in enumerate(parents):
            if np.random.rand() < self.config["mutation_rate"]:
                parents[idx] = next(generator)

    def _crossover_parents(self, parents: list[Individual]) -> list[Individual]:
        children = []

        for i in range(0, len(parents) - 1, 2):
            if np.random.rand() < self.config["crossover_rate"]:
                child1, child2 = self._crossover(parents[i], parents[i + 1])
                children.extend([child1, child2])
            else:
                children.extend([parents[i], parents[i + 1]])

        return children
    
    def _crossover(self, parent1, parent2):
        chosen_attr = np.random.choice(list(GeneticAttributes))

        child1_strategy = Strategy(
            (
                parent2.strategy.signal
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent1.strategy.signal
            ),
            (
                parent1.strategy.confirm
                if chosen_attr == GeneticAttributes.CONFIRM
                else parent2.strategy.confirm
            ),
            (
                parent1.strategy.pulse
                if chosen_attr == GeneticAttributes.PULSE
                else parent2.strategy.pulse
            ),
            (
                parent1.strategy.baseline
                if chosen_attr == GeneticAttributes.BASELINE
                else parent2.strategy.baseline
            ),
            (
                parent1.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent2.strategy.stop_loss
            ),
            (
                parent1.strategy.exit
                if chosen_attr == GeneticAttributes.EXIT
                else parent2.strategy.exit
            ),
        )
        child2_strategy = Strategy(
            (
                parent1.strategy.signal
                if chosen_attr == GeneticAttributes.SIGNAL
                else parent2.strategy.signal
            ),
            (
                parent2.strategy.confirm
                if chosen_attr == GeneticAttributes.CONFIRM
                else parent1.strategy.confirm
            ),
            (
                parent2.strategy.pulse
                if chosen_attr == GeneticAttributes.PULSE
                else parent1.strategy.pulse
            ),
            (
                parent2.strategy.baseline
                if chosen_attr == GeneticAttributes.BASELINE
                else parent1.strategy.baseline
            ),
            (
                parent2.strategy.stop_loss
                if chosen_attr == GeneticAttributes.STOP_LOSS
                else parent1.strategy.stop_loss
            ),
            (
                parent2.strategy.exit
                if chosen_attr == GeneticAttributes.EXIT
                else parent1.strategy.exit
            ),
        )

        parent1 = Individual(parent1.symbol, parent1.timeframe, child1_strategy)
        parent2 = Individual(parent2.symbol, parent2.timeframe, child2_strategy)

        return parent1, parent2