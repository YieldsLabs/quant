import asyncio
import logging
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


logger = logging.getLogger(__name__)


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

        self.default_timeframes = ["15m"]
        self.default_n_samples = 2
        self.elite_count = self.config.get("elite_count", 5)
        self.tournament_size = self.config.get("tournament_size", 3)
        self.mutation_rate = self.config.get("mutation_rate", 0.1)
        self.crossover_rate = self.config.get("crossover_rate", 0.7)
        self.reset_percentage = self.config.get("reset_percentage", 0.2)
        self.stability_percentage = self.config.get("stability_percentage", 0.3)

    async def on_receive(self, event: FactorEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(InitGeneration, self._init_generation)
        self.register_handler(GetGeneration, self._get_generation)
        self.register_handler(EnvolveGeneration, self._envolve_generation)

    async def _init_generation(self, msg: InitGeneration):
        generator = await self._get_generator(msg.datasource, msg.cap)
        population = list(generator)

        if not population:
            logger.warning("Initial population is empty.")
            return

        await self.state.set(self.POPULATION_KEY, population)
        await self.state.set(self.GENERATION_KEY, 0)

        logger.info(f"Initialized generation with {len(population)} individuals.")

    async def _get_generator(self, datasource, cap):
        symbols = await self.ask(GetSymbols(datasource, cap))
        timeframes = [
            Timeframe.from_raw(tf)
            for tf in self.config.get("timeframes", self.default_timeframes)
        ]
        return PopulationGenerator(
            symbols, timeframes, self.config.get("n_samples", self.default_n_samples)
        )

    async def _get_generation(
        self, _msg: GetGeneration
    ) -> Tuple[list[Tuple[Symbol, Timeframe, Strategy]], float]:
        population = [
            (ind.symbol, ind.timeframe, ind.strategy)
            for ind in await self.state.get(self.POPULATION_KEY, [])
        ]
        generation = await self.state.get(self.GENERATION_KEY, 0)

        logger.info(
            f"Generation: {generation + 1} with {[f"{p[0]}_{p[1]}{p[2]}" for p in population]}"
        )

        return population, generation

    async def _envolve_generation(self, msg: EnvolveGeneration):
        population = await self.state.get(self.POPULATION_KEY, [])
        generation = await self.state.get(self.GENERATION_KEY, 0)

        if not population:
            logger.warning("Population is empty. Skipping evolution.")
            return

        logger.info(f"Envolve generation: {generation + 1}")

        await self._evaluate_fitness(population)

        elite, parents = self._select_elite_and_parents(population)
        generator = await self._get_generator(msg.datasource, msg.cap)

        await self._mutate_parents(parents, generator)

        children = self._crossover_parents(parents)

        next_population = list(set(elite + children))
        next_generation = generation + 1

        await self.state.set(self.POPULATION_KEY, next_population)
        await self.state.set(self.GENERATION_KEY, next_generation)

        logger.info(
            f"Evolved to generation {next_generation + 1} with {len(next_population)} individuals."
        )

    async def _evaluate_fitness(self, population: List[Individual]) -> None:
        tasks = []
        for individual in population:
            task = self.ask(
                GetPortfolioPerformance(
                    individual.symbol, individual.timeframe, individual.strategy
                )
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for idx, ind in enumerate(population):
            ind.update_fitness(results[idx].deflated_sharpe_ratio)

        population[:] = [ind for ind in population if ind.fitness > 0]

    def _select_elite_and_parents(
        self, population: List[Individual]
    ) -> tuple[list[Individual], list[Individual]]:
        sorted_population = sorted(
            population, key=lambda ind: ind.fitness, reverse=True
        )
        elite = sorted_population[: self.elite_count]

        reset_size = int(self.reset_percentage * len(sorted_population))
        stability_size = int(self.stability_percentage * len(sorted_population))

        reset_parents = self._tournament_selection(sorted_population[:reset_size])
        stability_parents = self._tournament_selection(
            sorted_population[reset_size : reset_size + stability_size]
        )

        return elite, reset_parents + stability_parents

    def _tournament_selection(self, candidates: list[Individual]) -> list[Individual]:
        if not candidates:
            return []

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
            if np.random.rand() < self.mutation_rate:
                parents[idx] = next(generator)

    def _crossover_parents(self, parents: list[Individual]) -> list[Individual]:
        children = []

        for parent1, parent2 in zip(parents[::2], parents[1::2]):
            if np.random.rand() < self.crossover_rate:
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

        return (
            Individual(parent1.symbol, parent1.timeframe, child1_strategy),
            Individual(parent2.symbol, parent2.timeframe, child2_strategy),
        )
