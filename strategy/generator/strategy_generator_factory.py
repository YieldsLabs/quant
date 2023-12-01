from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.interfaces.abstract_strategy_generator_factory import (
    AbstractStrategyGeneratorFactory,
)
from core.models.strategy import StrategyType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.trend_follow import TrendFollowStrategyGenerator


class StrategyGeneratorFactory(AbstractStrategyGeneratorFactory):
    _generator_type = {StrategyType.TREND: TrendFollowStrategyGenerator}

    def __init__(
        self,
        config_service: AbstractConfig,
    ):
        super().__init__()
        self.config = config_service.get("generator")

    def create(
        self, type: StrategyType, symbols: list[Symbol]
    ) -> AbstractStrategyGenerator:
        if type not in self._generator_type:
            raise ValueError(f"Unknown StrategyType: {type}")

        generator_class = self._generator_type.get(type)

        _symbols = [
            symbol for symbol in symbols if symbol.name not in self.config["blacklist"]
        ]

        _timeframes = [
            Timeframe.from_raw(timeframe) for timeframe in self.config["timeframes"]
        ]

        return generator_class(self.config["n_samples"], _symbols, _timeframes)
