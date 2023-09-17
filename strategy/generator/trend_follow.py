from core.models.trend_candle import TrendCandleType
import numpy as np
from random import shuffle

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy

from ..indicator.ma import MovingAverageIndicator
from ..indicator.trend_candle import TrendCandleIndicator
from ..indicator.cross_ma import CrossMovingAverageIndicator
from ..indicator.testing_ground import TestingGroundIndicator
from ..stop_loss.atr import ATRStopLoss


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    STRATEGY_TYPES = ['crossma', 'candlema', 'ground']

    def __init__(self):
        super().__init__()

    def generate(self, n_samples):
        strategies = self._diversified_strategies() + self._random_strategies(n_samples)
        shuffle(strategies)
        
        return strategies

    def _diversified_strategies(self):
        atr_multi_values = [1.5]
        moving_average_periods = [(50, 100), (21, 34)]
        ma_types = [
            MovingAverageType.KAMA,
            MovingAverageType.HMA,
            MovingAverageType.ZLEMA,
        ]

        return [
            Strategy(
                'crossma', 
                (CrossMovingAverageIndicator(ma_type, StaticParameter(short_period), StaticParameter(long_period)),),
                ATRStopLoss(multi=StaticParameter(atr_multi_value))
            )
            for ma_type in ma_types
            for short_period, long_period in moving_average_periods
            for atr_multi_value in atr_multi_values
        ]
    
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
        long_period = RandomParameter(60.0, 200.0, 10.0)
        short_period, long_period = sorted([short_period, long_period])
        atr_multi = RandomParameter(0.85, 2, 0.05)

        if strategy_type == 'crossma':
            return Strategy(
                'crossma',
                (CrossMovingAverageIndicator(moving_avg_type, short_period, long_period),),
                ATRStopLoss(multi=atr_multi)
            )
        elif strategy_type == 'candlema':
            return Strategy(
                'candlema',
                (TrendCandleIndicator(trend_candle_type), MovingAverageIndicator(moving_avg_type, long_period),),
                ATRStopLoss(multi=atr_multi)
            )
        else:
            return Strategy(
                'ground',
                (TestingGroundIndicator(moving_avg_type, long_period),),
                ATRStopLoss(multi=atr_multi)
            )
