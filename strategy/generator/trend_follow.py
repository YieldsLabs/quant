from itertools import product
from random import shuffle
from symtable import Symbol

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import TrendCandleType
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy, StrategyType
from core.models.timeframe import Timeframe
from strategy.exit.dumb import DumbExit
from strategy.filter.adx import ADXFilter
from strategy.filter.fib import FibFilter
from strategy.filter.ma import MovingAverageFilter
from strategy.filter.macd import MACDFilter
from strategy.filter.ribbon import RibbonFilter
from strategy.filter.rsi import RSIFilter
from strategy.filter.stoch import StochFilter
from strategy.filter.supertrend import SupertrendFilter
from strategy.filter.tii import TIIFilter
from strategy.signal.ao_flip import AOFlipSignal
from strategy.signal.cc_flip import CCFlipSignal
from strategy.signal.dch_two_ma import DCH2MovingAverageSignal
from strategy.signal.di_cross import DICrossSignal
from strategy.signal.di_flip import DIFlipSignal
from strategy.signal.ma_three_cross import MA3CrossSignal
from strategy.signal.macd_color_switch import MACDColorSwitchSignal
from strategy.signal.macd_cross import MACDCrossSignal
from strategy.signal.macd_flip import MACDFlipSignal
from strategy.signal.qstick_cross import QSTICKCrossSignal
from strategy.signal.qstick_flip import QSTICKFlipSignal
from strategy.signal.quadruple import QuadrupleSignal
from strategy.signal.roc_flip import ROCFlipSignal
from strategy.signal.rsi_ma_pullback import RSIMovingAveragePullbackSignal
from strategy.signal.rsi_neutrality_cross import RSINautralityCrossSignal
from strategy.signal.rsi_neutrality_pullback import RSINautralityPullbackSignal
from strategy.signal.rsi_neutrality_rejection import RSINautralityRejectionSignal
from strategy.signal.rsi_two_ma import RSI2MovingAverageSignal
from strategy.signal.rsi_v import RSIVSignal
from strategy.signal.snatr import SNATRSignal
from strategy.signal.stc_flip import STCFlipSignal
from strategy.signal.supertrend_flip import SupertrendFlipSignal
from strategy.signal.supertrend_pullback import SupertrendPullBackSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.signal.tii_cross import TIICrossSignal
from strategy.signal.tii_v import TIIVSignal
from strategy.signal.trend_candle import TrendCandleSignal
from strategy.signal.trix_flip import TRIXFlipSignal
from strategy.signal.tsi_cross import TSICrossSignal
from strategy.signal.tsi_flip import TSIFlipSignal
from strategy.stop_loss.atr import ATRStopLoss


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    def __init__(
        self,
        n_samples: int,
        symbols: list[Symbol],
        timeframes: list[Timeframe],
    ):
        super().__init__()
        self.n_samples = n_samples
        self.timeframes = timeframes
        self.symbols = symbols

    def generate(self) -> list[tuple[Symbol, Timeframe, Strategy]]:
        strategies = self.generate_strategies()
        sampled_symbols = self.generate_symbols()
        sampled_timeframes = self.generate_timeframes()

        data = list(product(sampled_symbols, sampled_timeframes, strategies))

        shuffle(data)

        return data

    def generate_strategies(self) -> list[Strategy]:
        return self._diversified_strategies() + self._random_strategies()

    def generate_symbols(self) -> list[Symbol]:
        num_symbols_to_sample = min(self.n_samples, len(self.symbols))

        return np.random.choice(self.symbols, size=num_symbols_to_sample, replace=False)

    def generate_timeframes(self) -> list[Timeframe]:
        num_timeframes_to_sample = min(self.n_samples, len(self.timeframes))

        return np.random.choice(
            self.timeframes, size=num_timeframes_to_sample, replace=False
        )

    def _diversified_strategies(self):
        atr_period = StaticParameter(14.0)
        atr_multi = StaticParameter(0.85)
        strategies = [
            (
                StrategyType.TREND,
                TrendCandleSignal(
                    candle=StaticParameter(TrendCandleType.THREE_METHODS)
                ),
                MovingAverageFilter(
                    smoothing=StaticParameter(MovingAverageType.WMA),
                    period=StaticParameter(250.0),
                ),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.HEXAD)),
                MovingAverageFilter(
                    smoothing=StaticParameter(MovingAverageType.MD),
                    period=StaticParameter(150.0),
                ),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                TrendCandleSignal(
                    candle=StaticParameter(TrendCandleType.DOUBLE_TROUBLE)
                ),
                RSIFilter(),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.H)),
                TIIFilter(),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.GOLDEN)),
                TIIFilter(),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                TrendCandleSignal(candle=StaticParameter(TrendCandleType.BOTTLE)),
                StochFilter(),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
            (
                StrategyType.TREND,
                SupertrendFlipSignal(),
                RSIFilter(),
                ATRStopLoss(period=atr_period, multi=atr_multi),
                DumbExit(),
            ),
        ]

        return [Strategy(*strategy) for strategy in strategies]

    def _random_strategies(self):
        strategies_set = set()

        def add_strategy():
            strategy = self._generate_strategy()
            if strategy not in strategies_set:
                strategies_set.add(strategy)

        for _ in range(self.n_samples):
            add_strategy()

        remainders = self.n_samples - len(strategies_set)

        for _ in range(remainders):
            add_strategy()

        return list(strategies_set)

    def _generate_strategy(self):
        _short_period = RandomParameter(20.0, 50.0, 5.0)
        _long_period = RandomParameter(50.0, 200.0, 10.0)
        ma_medium_period = RandomParameter(50.0, 100.0, 5.0)
        ma_short_period, ma_long_period = sorted([_short_period, _long_period])
        ma_filter_period = RandomParameter(100.0, 300.0, 25.0)
        atr_multi = RandomParameter(1.0, 2, 0.25)

        filter = np.random.choice(
            [
                MovingAverageFilter(period=ma_filter_period),
                RSIFilter(),
                ADXFilter(),
                TIIFilter(),
                StochFilter(),
                SupertrendFilter(),
                MACDFilter(),
                RibbonFilter(),
                FibFilter(),
            ]
        )
        stop_loss = np.random.choice([ATRStopLoss(multi=atr_multi)])
        exit_signal = np.random.choice([DumbExit()])

        flip_signal = np.random.choice(
            [
                AOFlipSignal(),
                MACDFlipSignal(),
                SupertrendFlipSignal(),
                ROCFlipSignal(),
                TRIXFlipSignal(),
                TSIFlipSignal(),
                DIFlipSignal(),
                QSTICKFlipSignal(),
                CCFlipSignal(),
                STCFlipSignal(),
            ]
        )

        v_signal = np.random.choice([TIIVSignal(), RSIVSignal()])

        cross_signal = np.random.choice(
            [
                MA3CrossSignal(
                    short_period=ma_short_period,
                    medium_period=ma_medium_period,
                    long_period=ma_long_period,
                ),
                MACDCrossSignal(),
                TIICrossSignal(),
                RSINautralityCrossSignal(),
                TSICrossSignal(),
                DICrossSignal(),
                QSTICKCrossSignal(),
            ]
        )

        two_ma_signal = np.random.choice(
            [
                RSI2MovingAverageSignal(),
                DCH2MovingAverageSignal(),
            ]
        )

        pullback_signal = np.random.choice(
            [
                SupertrendPullBackSignal(),
                RSINautralityPullbackSignal(),
                RSIMovingAveragePullbackSignal(),
            ]
        )

        signal = np.random.choice(
            [
                MACDColorSwitchSignal(),
                TrendCandleSignal(),
                SNATRSignal(),
                RSINautralityRejectionSignal(),
                TestingGroundSignal(period=ma_long_period),
                flip_signal,
                v_signal,
                cross_signal,
                two_ma_signal,
                pullback_signal,
                QuadrupleSignal(),
            ]
        )

        return Strategy(*(StrategyType.TREND, signal, filter, stop_loss, exit_signal))
