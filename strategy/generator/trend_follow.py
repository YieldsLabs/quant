from enum import Enum, auto
from random import shuffle

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import TrendCandleType
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy
from strategy.exit.dumb import DumbExit
from strategy.filter.adx import ADXFilter
from strategy.filter.ma import MovingAverageFilter
from strategy.filter.macd import MACDFilter
from strategy.filter.rsi import RSIFilter
from strategy.filter.stoch import StochFilter
from strategy.filter.supertrend import SupertrendFilter
from strategy.filter.tii import TIIFilter
from strategy.signal.ma_three_cross import MA3CrossSignal
from strategy.signal.macd_flip import MACDFlipSignal
from strategy.signal.rsi_neutrality_cross import RSINautralityCrossSignal
from strategy.signal.rsi_neutrality_pullback import RSINautralityPullbackSignal
from strategy.signal.rsi_neutrality_rejection import RSINautralityRejectionSignal
from strategy.signal.rsi_two_ma import RSI2MovingAverageSignal
from strategy.signal.rsi_v import RSIVSignal
from strategy.signal.snatr import SNATRSignal
from strategy.signal.supertrend_flip import SupertrendFlipSignal
from strategy.signal.supertrend_pullback import SupertrendPullBackSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.signal.tii_cross import TIICrossSignal
from strategy.signal.trend_candle import TrendCandleSignal
from strategy.stop_loss.atr import ATRStopLoss


class StrategyTypes(Enum):
    ThreeMaCross = auto()
    TiiCross = auto()
    RsiNeutralityCross = auto()
    RsiNeutralityPullback = auto()
    RsiNeutralityRejection = auto()
    MACDFlip = auto()
    Ground = auto()
    SnAtr = auto()
    SupFlip = auto()
    SupPullBack = auto()
    TrendCandle = auto()
    Rsi2Ma = auto()
    RsiVMa = auto()


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    def __init__(self):
        super().__init__()

    def generate(self, n_samples):
        strategies = self._diversified_strategies() + self._random_strategies(n_samples)
        shuffle(strategies)

        return strategies

    def _diversified_strategies(self):
        strategies = [
            (
                TrendCandleSignal(
                    candle=StaticParameter(TrendCandleType.THREE_METHODS)
                ),
                MovingAverageFilter(
                    smoothing=StaticParameter(MovingAverageType.WMA),
                    period=StaticParameter(250.0),
                ),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(0.85)),
                DumbExit(),
            ),
            (
                TrendCandleSignal(
                    candle=StaticParameter(TrendCandleType.DOUBLE_TROUBLE)
                ),
                RSIFilter(),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(1.5)),
                DumbExit(),
            ),
            (
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.H)),
                TIIFilter(),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(1.5)),
                DumbExit(),
            ),
            (
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.HIKKAKE)),
                MovingAverageFilter(
                    smoothing=StaticParameter(MovingAverageType.ZLSMA),
                    period=StaticParameter(300.0),
                ),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(1.5)),
                DumbExit(),
            ),
            (
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.BOTTLE)),
                StochFilter(),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(1.5)),
                DumbExit(),
            ),
            (
                SupertrendFlipSignal(),
                RSIFilter(),
                ATRStopLoss(period=StaticParameter(14.0), multi=StaticParameter(1.5)),
                DumbExit(),
            ),
        ]

        return [Strategy(*strategy) for strategy in strategies]

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
        _short_period = RandomParameter(20.0, 50.0, 5.0)
        _long_period = RandomParameter(50.0, 200.0, 10.0)
        ma_medium_period = RandomParameter(50.0, 100.0, 5.0)
        ma_short_period, ma_long_period = sorted([_short_period, _long_period])
        ma_filter_period = RandomParameter(100.0, 300.0, 25.0)
        rsi_lower_barrier = RandomParameter(5.0, 15.0, 1.0)
        rsi_upper_barrier = RandomParameter(75.0, 95, 1.0)
        atr_multi = RandomParameter(0.85, 2, 0.05)

        filter = np.random.choice(
            [
                MovingAverageFilter(period=ma_filter_period),
                RSIFilter(),
                ADXFilter(),
                TIIFilter(),
                StochFilter(),
                SupertrendFilter(),
                MACDFilter(),
            ]
        )
        stop_loss = np.random.choice([ATRStopLoss(multi=atr_multi)])
        exit_signal = np.random.choice([DumbExit()])

        strategy_map = {
            StrategyTypes.ThreeMaCross: (
                MA3CrossSignal(
                    short_period=ma_short_period,
                    medium_period=ma_medium_period,
                    long_period=ma_long_period,
                ),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.MACDFlip: (
                MACDFlipSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.TiiCross: (TIICrossSignal(), filter, stop_loss, exit_signal),
            StrategyTypes.TrendCandle: (
                TrendCandleSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.SnAtr: (SNATRSignal(), filter, stop_loss, exit_signal),
            StrategyTypes.SupFlip: (
                SupertrendFlipSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.SupPullBack: (
                SupertrendPullBackSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.Rsi2Ma: (
                RSI2MovingAverageSignal(
                    lower_barrier=rsi_lower_barrier,
                    upper_barrier=rsi_upper_barrier,
                ),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.RsiNeutralityCross: (
                RSINautralityCrossSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.RsiNeutralityPullback: (
                RSINautralityPullbackSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.RsiNeutralityRejection: (
                RSINautralityRejectionSignal(),
                filter,
                stop_loss,
                exit_signal,
            ),
            StrategyTypes.RsiVMa: (
                RSIVSignal(
                    lower_barrier=rsi_lower_barrier, upper_barrier=rsi_upper_barrier
                ),
                filter,
                stop_loss,
                exit_signal,
            ),
        }

        strategy_tuple = strategy_map.get(
            strategy_type,
            (
                TestingGroundSignal(period=ma_long_period),
                filter,
                stop_loss,
                exit_signal,
            ),
        )

        return Strategy(*strategy_tuple)
