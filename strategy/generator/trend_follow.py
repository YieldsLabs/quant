from enum import Enum, auto
from itertools import product
from random import shuffle
from symtable import Symbol

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy, StrategyType
from core.models.timeframe import Timeframe
from strategy.baseline.ma import MaBaseLine
from strategy.exit.ast import AstExit
from strategy.exit.ce import CeExit
from strategy.exit.dumb import DumbExit
from strategy.exit.highlow import HighLowExit
from strategy.exit.ma import MaExit
from strategy.exit.pattern import PatternExit
from strategy.exit.rsi import RsiExit
from strategy.filter.apo import ApoFilter
from strategy.filter.bop import BopFilter
from strategy.filter.braid import BraidFilter
from strategy.filter.dpo import DpoFilter
from strategy.filter.eis import EisFilter
from strategy.filter.eom import EomFilter
from strategy.filter.fib import FibFilter
from strategy.filter.kst import KstFilter
from strategy.filter.macd import MacdFilter
from strategy.filter.ribbon import RibbonFilter
from strategy.filter.rsi import RsiFilter
from strategy.filter.stoch import StochFilter
from strategy.filter.supertrend import SupertrendFilter
from strategy.filter.tii import TiiFilter
from strategy.pulse.adx import AdxPulse
from strategy.pulse.chop import ChopPulse
from strategy.pulse.dumb import DumbPulse
from strategy.pulse.vo import VoPulse
from strategy.signal.ao_flip import AoFlipSignal
from strategy.signal.ao_saucer import AoSaucerSignal
from strategy.signal.apo_flip import ApoFlipSignal
from strategy.signal.bop_flip import BopFlipSignal
from strategy.signal.cc_flip import CcFlipSignal
from strategy.signal.cfo_flip import CfoFlipSignal
from strategy.signal.dch_two_ma import Dch2MaSignal
from strategy.signal.di_cross import DiCrossSignal
from strategy.signal.di_flip import DiFlipSignal
from strategy.signal.dmi_cross import DmiCrossSignal
from strategy.signal.hl import HighLowSignal
from strategy.signal.kst_cross import KstCrossSignal
from strategy.signal.ma_three_cross import Ma3CrossSignal
from strategy.signal.macd_color_switch import MacdColorSwitchSignal
from strategy.signal.macd_cross import MacdCrossSignal
from strategy.signal.macd_flip import MacdFlipSignal
from strategy.signal.qstick_cross import QstickCrossSignal
from strategy.signal.qstick_flip import QstickFlipSignal
from strategy.signal.quadruple import QuadrupleSignal
from strategy.signal.roc_flip import RocFlipSignal
from strategy.signal.rsi_ma_pullback import RsiMaPullbackSignal
from strategy.signal.rsi_neutrality_cross import RsiNautralityCrossSignal
from strategy.signal.rsi_neutrality_pullback import RsiNautralityPullbackSignal
from strategy.signal.rsi_neutrality_rejection import RsiNautralityRejectionSignal
from strategy.signal.rsi_two_ma import Rsi2MaSignal
from strategy.signal.rsi_v import RsiVSignal
from strategy.signal.snatr import SnatrSignal
from strategy.signal.stc_flip import StcFlipSignal
from strategy.signal.stc_uturn import StcUTurnSignal
from strategy.signal.stoch_cross import StochCrossSignal
from strategy.signal.supertrend_flip import SupertrendFlipSignal
from strategy.signal.supertrend_pullback import SupertrendPullBackSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.signal.tii_cross import TiiCrossSignal
from strategy.signal.tii_v import TiiVSignal
from strategy.signal.trend_candle import TrendCandleSignal
from strategy.signal.trix_cross import TrixCrossSignal
from strategy.signal.trix_flip import TrixFlipSignal
from strategy.signal.tsi_cross import TsiCrossSignal
from strategy.signal.tsi_flip import TsiFlipSignal
from strategy.signal.vwap_cross import VwapCrossSignal
from strategy.stop_loss.atr import AtrStopLoss


class TrendSignalType(Enum):
    CROSS = auto()
    FLIP = auto()
    V = auto()
    UTurn = auto()
    TWO_MA = auto()
    CUSTOM = auto()
    PULLBACK = auto()


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
        return []

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
        signal_groups = list(TrendSignalType)
        entry_signal = self._generate_signal(np.random.choice(signal_groups))
        filter = np.random.choice(
            [
                RsiFilter(),
                TiiFilter(),
                StochFilter(),
                SupertrendFilter(),
                MacdFilter(),
                RibbonFilter(),
                FibFilter(),
                EisFilter(),
                BraidFilter(),
                ApoFilter(),
                BopFilter(),
                DpoFilter(),
                KstFilter(),
                EomFilter(),
            ]
        )
        pulse = np.random.choice([DumbPulse(), AdxPulse(), ChopPulse(), VoPulse()])
        baseline = np.random.choice(
            [
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.EMA),
                    period=RandomParameter(100.0, 150.0, 10.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.WMA),
                    period=RandomParameter(15.0, 30.0, 1.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.SMMA),
                    period=RandomParameter(100.0, 150.0, 10.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.HMA),
                    period=RandomParameter(86.0, 90.0, 1.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.DEMA),
                    period=RandomParameter(26.0, 30.0, 1.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.KAMA),
                    period=RandomParameter(30.0, 50.0, 1.0),
                ),
                MaBaseLine(
                    smoothing=StaticParameter(MovingAverageType.KIJUN),
                    period=RandomParameter(30.0, 40.0, 1.0),
                ),
            ]
        )
        stop_loss = np.random.choice(
            [AtrStopLoss(multi=RandomParameter(0.85, 1.8, 0.15))]
        )
        exit_signal = np.random.choice(
            [
                AstExit(),
                CeExit(),
                DumbExit(),
                PatternExit(),
                HighLowExit(),
                MaExit(),
                RsiExit(),
            ]
        )

        return Strategy(
            *(
                StrategyType.TREND,
                entry_signal,
                filter,
                pulse,
                baseline,
                stop_loss,
                exit_signal,
            )
        )

    def _generate_signal(self, signal: TrendSignalType):
        ma_short_period, ma_medium_period, ma_long_period = sorted(
            [
                RandomParameter(20.0, 50.0, 5.0),
                RandomParameter(50.0, 100.0, 5.0),
                RandomParameter(50.0, 200.0, 10.0),
            ]
        )

        if signal == TrendSignalType.FLIP:
            return np.random.choice(
                [
                    AoFlipSignal(),
                    MacdFlipSignal(),
                    SupertrendFlipSignal(),
                    RocFlipSignal(),
                    TrixFlipSignal(),
                    TsiFlipSignal(),
                    DiFlipSignal(),
                    QstickFlipSignal(),
                    CcFlipSignal(),
                    StcFlipSignal(),
                    ApoFlipSignal(),
                    BopFlipSignal(),
                    CfoFlipSignal(),
                ]
            )
        if signal == TrendSignalType.V:
            return np.random.choice([TiiVSignal(), RsiVSignal()])

        if signal == TrendSignalType.UTurn:
            return np.random.choice([StcUTurnSignal()])

        if signal == TrendSignalType.CROSS:
            return np.random.choice(
                [
                    Ma3CrossSignal(
                        short_period=ma_short_period,
                        medium_period=ma_medium_period,
                        long_period=ma_long_period,
                    ),
                    MacdCrossSignal(),
                    TiiCrossSignal(),
                    RsiNautralityCrossSignal(),
                    TsiCrossSignal(),
                    DiCrossSignal(),
                    QstickCrossSignal(),
                    VwapCrossSignal(),
                    DmiCrossSignal(),
                    StochCrossSignal(),
                    KstCrossSignal(),
                    TrixCrossSignal(),
                ]
            )
        if signal == TrendSignalType.TWO_MA:
            return np.random.choice(
                [
                    Rsi2MaSignal(),
                    Dch2MaSignal(),
                ]
            )
        if signal == TrendSignalType.PULLBACK:
            return np.random.choice(
                [
                    SupertrendPullBackSignal(),
                    RsiNautralityPullbackSignal(),
                    RsiMaPullbackSignal(),
                ]
            )

        return np.random.choice(
            [
                AoSaucerSignal(),
                MacdColorSwitchSignal(),
                TrendCandleSignal(),
                SnatrSignal(),
                RsiNautralityRejectionSignal(),
                TestingGroundSignal(period=ma_long_period),
                QuadrupleSignal(),
                HighLowSignal(),
            ]
        )
