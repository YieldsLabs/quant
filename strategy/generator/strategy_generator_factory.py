from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.strategy import StrategyType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.trend_follow import TrendFollowStrategyGenerator


class StrategyGeneratorFactory(AbstractStrategyGeneratorFactory):
    def __init__(
        self, n_samples: int, symbols_blacklist: list[str], timeframes: list[Timeframe]
    ):
        super().__init__()
        self.n_samples = n_samples
        self.symbols_blacklist = symbols_blacklist
        self.timeframes = timeframes

    _generator_type = {StrategyType.TREND: TrendFollowStrategyGenerator}

    def create(
        self, type: StrategyType, symbols: list[Symbol]
    ) -> AbstractStrategyGenerator:
        if type not in self._generator_type:
            raise ValueError(f"Unknown StrategyType: {type}")

        generator_class = self._generator_type.get(type)

        _symbols = [
            symbol for symbol in symbols if symbol.name not in self.symbols_blacklist
        ]

        return generator_class(self.n_samples, _symbols, self.timeframes)
