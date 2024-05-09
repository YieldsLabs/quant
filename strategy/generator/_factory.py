from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .bootstrap._trend_follow import TrendFollowStrategyGenerator


class StrategyGeneratorFactory(AbstractStrategyGeneratorFactory):
    def __init__(
        self,
        config_service: AbstractConfig,
    ):
        super().__init__()
        self.config = config_service.get("generator")

    def create(self, symbols: list[Symbol]) -> AbstractStrategyGenerator:
        _symbols = [
            symbol for symbol in symbols if symbol.name not in self.config["blacklist"]
        ]

        _timeframes = [
            Timeframe.from_raw(timeframe) for timeframe in self.config["timeframes"]
        ]

        return TrendFollowStrategyGenerator(
            self.config["n_samples"], _symbols, _timeframes
        )
