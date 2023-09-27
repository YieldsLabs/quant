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
from strategy.signal.cross_three_ma import Cross3MovingAverageSignal
from strategy.signal.cross_two_ma import Cross2MovingAverageSignal
from strategy.signal.rsi import RSINautralitySignal
from strategy.signal.rsi_ma import RSIMovingAverageSignal
from strategy.signal.rsi_two_ma import RSI2MovingAverageSignal
from strategy.signal.snatr import SNATRSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.stop_loss.atr import ATRStopLoss


class StrategyTypes(Enum):
    Cross2xMa = auto()
    Cross3xMa = auto()
    CrossRsiNeutrality = auto()
    Ground = auto()
    SnAtr = auto()
    Candle = auto()
    RsiMa = auto()
    Rsi2xMa = auto()


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    STRATEGY_TYPES = list(StrategyTypes)

    def __init__(self):
        super().__init__()

    def generate(self, n_samples):
        strategies = self._diversified_strategies() + self._random_strategies(n_samples)
        shuffle(strategies)

        return strategies

    def _diversified_strategies(self):
        return []

    def _random_strategies(self, n_samples):
        strategies_set = set()

        num_per_type = n_samples // len(self.STRATEGY_TYPES)

        for strategy_type in self.STRATEGY_TYPES:
            count = 0
            while count < num_per_type:
                strategy = self._generate_strategy(strategy_type)
                if strategy not in strategies_set:
                    strategies_set.add(strategy)
                    count += 1

        remainders = n_samples - len(strategies_set)

        for _ in range(remainders):
            strategy_type = np.random.choice(self.STRATEGY_TYPES)
            strategy = self._generate_strategy(strategy_type)
            strategies_set.add(strategy)

        return list(strategies_set)

    def _generate_strategy(self, strategy_type):
        moving_avg_type = np.random.choice(list(MovingAverageType))
        trend_candle_type = np.random.choice(list(TrendCandleType))
        short_period = RandomParameter(20.0, 50.0, 5.0)
        medium_period = RandomParameter(50.0, 100.0, 5.0)
        long_period = RandomParameter(50.0, 200.0, 10.0)
        rsi_lower_barrier = RandomParameter(5.0, 15.0, 1.0)
        rsi_upper_barrier = RandomParameter(75.0, 95, 1.0)
        short_period, long_period = sorted([short_period, long_period])
        atr_multi = RandomParameter(0.85, 2, 0.05)

        filter = np.random.choice([MovingAverageFilter(moving_avg_type, long_period)])

        if strategy_type == StrategyTypes.Cross2xMa:
            return Strategy(
                "cross2ma",
                Cross2MovingAverageSignal(moving_avg_type, short_period, long_period),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )

        elif strategy_type == StrategyTypes.Cross3xMa:
            return Strategy(
                "cross3ma",
                Cross3MovingAverageSignal(
                    moving_avg_type, short_period, medium_period, long_period
                ),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )
        elif strategy_type == StrategyTypes.CrossRsiNeutrality:
            return Strategy(
                "rsicrossn",
                RSINautralitySignal(),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )
        elif strategy_type == StrategyTypes.Candle:
            return Strategy(
                "candle",
                TrendCandleSignal(trend_candle_type),
                filter,
                ATRStopLoss(multi=atr_multi),
            )

        elif strategy_type == StrategyTypes.SnAtr:
            return Strategy(
                "snatr",
                SNATRSignal(),
                MovingAverageFilter(moving_avg_type, long_period),
                ATRStopLoss(multi=atr_multi),
            )

        elif strategy_type == StrategyTypes.RsiMa:
            return Strategy(
                "rsima",
                RSIMovingAverageSignal(ma=moving_avg_type, period=short_period),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )

        elif strategy_type == StrategyTypes.Rsi2xMa:
            return Strategy(
                "rsi2ma",
                RSI2MovingAverageSignal(
                    ma=moving_avg_type,
                    lower_barrier=rsi_lower_barrier,
                    upper_barrier=rsi_upper_barrier,
                ),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )
        else:
            return Strategy(
                "ground",
                TestingGroundSignal(moving_avg_type, long_period),
                DumbFilter(),
                ATRStopLoss(multi=atr_multi),
            )
