from enum import Enum, auto
from typing import List, Tuple, Union

import numpy as np

from coral import DataSourceFactory
from core.actors import BaseActor
from core.actors.state import InMemory
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

    def __str__(self):
        return self.name.lower()

    @classmethod
    def all(cls):
        return list(cls)


class FactorActor(BaseActor, EventHandlerMixin):
    POPULATION_KEY = "__population__"
    GENERATION_KEY = "__generation__"

    def __init__(self, datasource: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.datasource = datasource
        self.config = config_service.get("factor")
        self.state = InMemory[str, Union[List[Individual], int]]()

    async def on_receive(self, event: FactorEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(InitGeneration, self._init_generation)
        self.register_handler(GetGeneration, self._get_generation)
        self.register_handler(EnvolveGeneration, self._envolve_generation)

    async def _init_generation(self, msg: InitGeneration):
        generator = await self._get_generator(msg.datasource, msg.cap)
        population = list(generator)

        await self.state.set(self.POPULATION_KEY, population)
        await self.state.set(self.GENERATION_KEY, 0)

    async def _get_generator(self, datasource, cap):
        symbols = await self.ask(GetSymbols(datasource, cap))

        timeframes = [
            Timeframe.from_raw(timeframe)
            for timeframe in self.config.get("timeframes", ["15m"])
        ]

        return PopulationGenerator(symbols, timeframes, self.config.get("n_samples", 2))

    async def _get_generation(
        self, _msg: GetGeneration
    ) -> Tuple[list[Tuple[Symbol, Timeframe, Strategy]], float]:
        population = [
            (i.symbol, i.timeframe, i.strategy)
            for i in await self.state.get(self.POPULATION_KEY, [])
        ]
        generation = await self.state.get(self.GENERATION_KEY, 0)

        return population, generation

    async def _envolve_generation(self, msg: EnvolveGeneration):
        population = await self.state.get(self.POPULATION_KEY, [])

        generator = await self._get_generator(msg.datasource, msg.cap)

        await self._evaluate_fitness(population)

        elite, parents = self._select_elite_and_parents(population)

        await self._mutate_parents(parents, generator)

        children = self._crossover_parents(parents)

        next_population = list(set(elite + children))
        next_generation = (await self.state.get(self.GENERATION_KEY, 0)) + 1

        await self.state.set(self.POPULATION_KEY, next_population)
        await self.state.set(self.GENERATION_KEY, next_generation)

    async def _evaluate_fitness(self, population: List[Individual]) -> None:
        for individual in population:
            performance = await self.ask(
                GetPortfolioPerformance(
                    individual.symbol, individual.timeframe, individual.strategy
                )
            )
            individual.update_fitness(performance.deflated_sharpe_ratio)

        population[:] = [ind for ind in population if ind.fitness > 0]

    def _select_elite_and_parents(
        self, population: List[Individual]
    ) -> tuple[list[Individual], list[Individual]]:
        sorted_population = sorted(
            population, key=lambda ind: ind.fitness, reverse=True
        )
        elite = sorted_population[: self.config.get("elite_count", 5)]

        total_size = len(sorted_population)
        reset_size = int(self.config.get("reset_percentage", 0.2) * total_size)
        stability_size = int(self.config.get("stability_percentage", 0.3) * total_size)

        reset_parents = self._tournament_selection(sorted_population[:reset_size])
        stability_parents = self._tournament_selection(
            sorted_population[reset_size : reset_size + stability_size]
        )

        return elite, reset_parents + stability_parents

    def _tournament_selection(self, candidates: list[Individual]) -> list[Individual]:
        parents = []

        tournament_size = min(len(candidates), self.config.get("tournament_size", 3))

        for _ in range(len(candidates)):
            contenders = np.random.choice(
                candidates, size=tournament_size, replace=False
            )
            parents.append(max(contenders, key=lambda ind: ind.fitness))

        return parents

    async def _mutate_parents(self, parents: list[Individual], generator) -> None:
        for idx, _ in enumerate(parents):
            if np.random.rand() < self.config.get("mutation_rate", 0.1):
                parents[idx] = next(generator)

    def _crossover_parents(self, parents: list[Individual]) -> list[Individual]:
        children = []

        for parent1, parent2 in zip(parents[::2], parents[1::2]):
            if np.random.rand() < self.config.get("crossover_rate", 0.7):
                child1, child2 = self._crossover(parent1, parent2)
                children.extend([child1, child2])
            else:
                children.extend([parent1, parent2])

        return children

    def _crossover(self, parent1, parent2):
        chosen_attrs = np.random.choice(GeneticAttributes.all(), size=2, replace=False)

        child1_strategy = Strategy(
            **{
                attr.name.lower(): (
                    getattr(parent2.strategy, attr.name.lower())
                    if attr in chosen_attrs
                    else getattr(parent1.strategy, attr.name.lower())
                )
                for attr in GeneticAttributes
            }
        )
        child2_strategy = Strategy(
            **{
                attr.name.lower(): (
                    getattr(parent1.strategy, attr.name.lower())
                    if attr in chosen_attrs
                    else getattr(parent2.strategy, attr.name.lower())
                )
                for attr in GeneticAttributes
            }
        )

        parent1 = Individual(parent1.symbol, parent1.timeframe, child1_strategy)
        parent2 = Individual(parent2.symbol, parent2.timeframe, child2_strategy)

        return parent1, parent2
