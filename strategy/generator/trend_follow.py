from enum import Enum, auto
from random import shuffle

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import TrendCandleType
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter
from core.models.strategy import Strategy
from strategy.filter.dumb import DumbFilter
from strategy.filter.ma import MovingAverageFilter
from strategy.signal.candle import TrendCandleSignal
from strategy.signal.cross_rsi_neutrality import CrossRSINautralitySignal
from strategy.signal.cross_three_ma import Cross3MovingAverageSignal
from strategy.signal.cross_tii import CrossTIISignal
from strategy.signal.rsi_two_ma import RSI2MovingAverageSignal
from strategy.signal.snatr import SNATRSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.stop_loss.atr import ATRStopLoss


class StrategyTypes(Enum):
    Cross3Ma = auto()
    CrossTii = auto()
    Ground = auto()
    SnAtr = auto()
    Candle = auto()
    Rsi2Ma = auto()
    CrossRsiN = auto()


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    def __init__(self):
        super().__init__()

    def generate(self, n_samples):
        strategies = self._diversified_strategies() + self._random_strategies(n_samples)
        shuffle(strategies)

        return strategies

    def _diversified_strategies(self):
        return []

    def _random_strategies(self, n_samples):
        strategy_types = list(StrategyTypes)
        strategies_set = set()

        num_per_type = n_samples // len(strategy_types)

        def add_strategy(strategy_type):
            strategy = self._generate_strategy(strategy_type)
            if strategy not in strategies_set:
                strategies_set.add(strategy)

        for strategy_type in strategy_types:
            for _ in range(num_per_type):
                add_strategy(strategy_type)

        remainders = n_samples - len(strategies_set)

        for _ in range(remainders):
            strategy_type = np.random.choice(strategy_types)
            add_strategy(strategy_type)

        return list(strategies_set)

    def _generate_strategy(self, strategy_type):
        moving_avg_type = np.random.choice(list(MovingAverageType))
        trend_candle_type = np.random.choice(list(TrendCandleType))
        _short_period = RandomParameter(20.0, 50.0, 5.0)
        _long_period = RandomParameter(50.0, 200.0, 10.0)
        ma_medium_period = RandomParameter(50.0, 100.0, 5.0)
        ma_short_period, ma_long_period = sorted([_short_period, _long_period])
        ma_filter_period = RandomParameter(50.0, 200.0, 50.0)
        rsi_lower_barrier = RandomParameter(5.0, 15.0, 1.0)
        rsi_upper_barrier = RandomParameter(75.0, 95, 1.0)
        atr_multi = RandomParameter(0.85, 2, 0.05)

        ma_filter = np.random.choice(
            [MovingAverageFilter(moving_avg_type, ma_filter_period)]
        )

        stop_loss = np.random.choice([ATRStopLoss(multi=atr_multi)])

        strategy_map = {
            StrategyTypes.Cross3Ma: (
                "cross3ma",
                Cross3MovingAverageSignal(
                    moving_avg_type, ma_short_period, ma_medium_period, ma_long_period
                ),
                DumbFilter(),
                stop_loss,
            ),
            StrategyTypes.CrossTii: (
                "crosstii",
                CrossTIISignal(),
                ma_filter,
                stop_loss,
            ),
            StrategyTypes.Candle: (
                "candle",
                TrendCandleSignal(trend_candle_type),
                ma_filter,
                stop_loss,
            ),
            StrategyTypes.SnAtr: (
                "snatr",
                SNATRSignal(),
                ma_filter,
                stop_loss,
            ),
            StrategyTypes.Rsi2Ma: (
                "rsi2ma",
                RSI2MovingAverageSignal(
                    ma=moving_avg_type,
                    lower_barrier=rsi_lower_barrier,
                    upper_barrier=rsi_upper_barrier,
                ),
                DumbFilter(),
                stop_loss,
            ),
            StrategyTypes.CrossRsiN: (
                "crossrsin",
                CrossRSINautralitySignal(),
                DumbFilter(),
                stop_loss,
            ),
        }

        strategy_tuple = strategy_map.get(
            strategy_type,
            (
                "ground",
                TestingGroundSignal(moving_avg_type, ma_long_period),
                DumbFilter(),
                stop_loss,
            ),
        )

        return Strategy(*strategy_tuple)
