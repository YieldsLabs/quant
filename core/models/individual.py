from dataclasses import dataclass

from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe


@dataclass
class Individual:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    fitness: float = 0.0

    def update_fitness(self, value):
        self.fitness = value
