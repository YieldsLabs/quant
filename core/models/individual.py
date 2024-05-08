from dataclasses import dataclass

from .strategy import Strategy
from .symbol import Symbol
from .timeframe import Timeframe

# TODO: use private fields


@dataclass
class Individual:
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    fitness: float = 0.0

    def update_fitness(self, value):
        self.fitness = value

    def __hash__(self) -> int:
        return hash(f"{self.symbol}_{self.timeframe}{self.strategy}")

    def __str__(self):
        return f"{self.symbol}_{self.timeframe}{self.strategy}"
