from enum import Enum, auto
from itertools import product
from random import shuffle
from typing import List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.baseline.ma import MaBaseLine
from strategy.generator.confirm.bb import BbConfirm
from strategy.generator.confirm.braid import BraidConfirm
from strategy.generator.confirm.cc import CcConfirm
from strategy.generator.confirm.cci import CciConfirm
from strategy.generator.confirm.didi import DidiConfirm
from strategy.generator.confirm.dpo import DpoConfirm
from strategy.generator.confirm.dumb import DumbConfirm
from strategy.generator.confirm.eom import EomConfirm
from strategy.generator.confirm.rsi_signalline import RsiSignalLineConfirm
from strategy.generator.confirm.stc import StcConfirm
from strategy.generator.confirm.wpr import WprConfirm
from strategy.generator.exit.highlow import HighLowExit
from strategy.generator.exit.mad import MadExit
from strategy.generator.exit.rex import RexExit
from strategy.generator.exit.trix import TrixExit
from strategy.generator.pulse.adx import AdxPulse
from strategy.generator.pulse.chop import ChopPulse
from strategy.generator.pulse.dumb import DumbPulse
from strategy.generator.pulse.nvol import NvolPulse
from strategy.generator.pulse.sqz import SqzPulse
from strategy.generator.pulse.tdfi import TdfiPulse
from strategy.generator.pulse.vo import VoPulse
from strategy.generator.pulse.wae import WaePulse
from strategy.generator.pulse.yz import YzPulse
from strategy.generator.signal.bb.macd import MacdBbSignal
from strategy.generator.signal.bb.vwap import VwapBbSignal
from strategy.generator.signal.breakout.dch_two_ma import DchMa2BreakoutSignal
from strategy.generator.signal.colorswitch.macd import MacdColorSwitchSignal
from strategy.generator.signal.contrarian.kch_a import KchASignal
from strategy.generator.signal.contrarian.kch_c import KchCSignal
from strategy.generator.signal.contrarian.rsi_c import RsiCSignal
from strategy.generator.signal.contrarian.rsi_d import RsiDSignal
from strategy.generator.signal.contrarian.rsi_nt import RsiNtSignal
from strategy.generator.signal.contrarian.rsi_u import RsiUSignal
from strategy.generator.signal.contrarian.rsi_v import RsiVSignal
from strategy.generator.signal.contrarian.snatr import SnatrSignal
from strategy.generator.signal.contrarian.stoch_e import StochESignal
from strategy.generator.signal.contrarian.tii_v import TiiVSignal
from strategy.generator.signal.flip.ce import CeFlipSignal
from strategy.generator.signal.flip.supertrend import SupertrendFlipSignal
from strategy.generator.signal.ma.ma2_rsi import Ma2RsiSignal
from strategy.generator.signal.ma.ma3_cross import Ma3CrossSignal
from strategy.generator.signal.ma.ma_cross import MaCrossSignal
from strategy.generator.signal.ma.ma_quadruple import MaQuadrupleSignal
from strategy.generator.signal.ma.ma_surpass import MaSurpassSignal
from strategy.generator.signal.ma.ma_testing_ground import MaTestingGroundSignal
from strategy.generator.signal.ma.vwap_cross import VwapCrossSignal
from strategy.generator.signal.neutrality.dso_cross import DsoNeutralityCrossSignal
from strategy.generator.signal.neutrality.rsi_cross import RsiNautralityCrossSignal
from strategy.generator.signal.neutrality.rsi_pullback import (
    RsiNautralityPullbackSignal,
)
from strategy.generator.signal.neutrality.rsi_rejection import (
    RsiNautralityRejectionSignal,
)
from strategy.generator.signal.neutrality.tii_cross import TiiNeutralityCrossSignal
from strategy.generator.signal.pattern.ao_saucer import AoSaucerSignal
from strategy.generator.signal.pattern.candle_reversal import CandlestickReversalSignal
from strategy.generator.signal.pattern.candle_trend import CandlestickTrendSignal
from strategy.generator.signal.pattern.hl import HighLowSignal
from strategy.generator.signal.signalline.di import DiSignalLineSignal
from strategy.generator.signal.signalline.dso import DsoSignalLineSignal
from strategy.generator.signal.signalline.kst import KstSignalLineSignal
from strategy.generator.signal.signalline.macd import MacdSignalLineSignal
from strategy.generator.signal.signalline.qstick import QstickSignalLineSignal
from strategy.generator.signal.signalline.rsi import RsiSignalLineSignal
from strategy.generator.signal.signalline.stoch import StochSignalLineSignal
from strategy.generator.signal.signalline.trix import TrixSignalLineSignal
from strategy.generator.signal.signalline.tsi import TsiSignalLineSignal
from strategy.generator.signal.twolinescross.dmi import Dmi2LinesCrossSignal
from strategy.generator.signal.twolinescross.vi import Vi2LinesCrossSignal
from strategy.generator.signal.zerocross.ao import AoZeroCrossSignal
from strategy.generator.signal.zerocross.bop import BopZeroCrossSignal
from strategy.generator.signal.zerocross.cc import CcZeroCrossSignal
from strategy.generator.signal.zerocross.cfo import CfoZeroCrossSignal
from strategy.generator.signal.zerocross.macd import MacdZeroCrossSignal
from strategy.generator.signal.zerocross.mad import MadZeroCrossSignal
from strategy.generator.signal.zerocross.qstick import QstickZeroCrossSignal
from strategy.generator.signal.zerocross.roc import RocZeroCrossSignal
from strategy.generator.signal.zerocross.trix import TrixZeroCrossSignal
from strategy.generator.signal.zerocross.tsi import TsiZeroCrossSignal
from strategy.generator.stop_loss.atr import AtrStopLoss


class TrendSignalType(Enum):
    ZERO_CROSS = auto()
    SIGNAL_LINE = auto()
    LINES_TWO_CROSS = auto()
    CONTRARIAN = auto()
    BB = auto()
    PATTERN = auto()
    COLOR_SWITCH = auto()
    FLIP = auto()
    MA = auto()
    BREAKOUT = auto()
    NEUTRALITY = auto()


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
        sampled_symbols = self.generate_symbols()
        sampled_timeframes = self.generate_timeframes()
        strategies = self.generate_strategies()

        data = list(set(product(sampled_symbols, sampled_timeframes, strategies)))

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
            base_strategy = self._generate_strategy()

            if base_strategy not in strategies_set:
                invariants = self._generate_invariants(base_strategy)

                for strategy in invariants:
                    if strategy not in strategies_set:
                        strategies_set.add(strategy)

        for _ in range(self.n_samples):
            add_strategy()

        remainders = self.n_samples - len(strategies_set)

        if remainders > 0:
            for _ in range(remainders):
                add_strategy()

        return list(strategies_set)

    def _generate_strategy(self):
        signal_groups = list(TrendSignalType)
        entry_signal = self._generate_signal(np.random.choice(signal_groups))
        baseline = np.random.choice(
            [
                MaBaseLine(),
            ]
        )
        confirm = np.random.choice(
            [
                DpoConfirm(),
                EomConfirm(),
                WprConfirm(),
                CciConfirm(),
                BraidConfirm(),
                RsiSignalLineConfirm(),
                CcConfirm(),
                DumbConfirm(),
                BbConfirm(),
                DidiConfirm(),
                StcConfirm(),
            ]
        )
        pulse = np.random.choice(
            [
                AdxPulse(),
                ChopPulse(),
                VoPulse(),
                NvolPulse(),
                TdfiPulse(),
                WaePulse(),
                YzPulse(),
                SqzPulse(),
                DumbPulse(),
            ]
        )
        stop_loss = np.random.choice([AtrStopLoss()])
        exit_signal = np.random.choice(
            [
                HighLowExit(),
                TrixExit(),
                RexExit(),
                MadExit(),
            ]
        )

        return Strategy(
            *(
                entry_signal,
                confirm,
                pulse,
                baseline,
                stop_loss,
                exit_signal,
            )
        )

    def _generate_invariants(self, base_strategy: Strategy) -> List[Strategy]:
        result = [base_strategy]
        # strategy_attributes = []

        # def smooth_invariants(strategy_part, nums=8):
        #     smooth_attr = ["smooth_type", "smooth_signal", "smooth_bb"]
        #     replacements = []

        #     for attr in smooth_attr:
        #         if hasattr(strategy_part, attr):
        #             replacements.extend(
        #                 [
        #                     replace(
        #                         strategy_part, **{attr: CategoricalParameter(Smooth)}
        #                     )
        #                     for _ in range(nums)
        #                 ]
        #             )

        #     return replacements

        # def candle_invariants(strategy_part, nums=3):
        #     smooth_attr = ["candle"]
        #     replacements = []

        #     for attr in smooth_attr:
        #         if hasattr(strategy_part, attr):
        #             replacements.extend(
        #                 [
        #                     replace(
        #                         strategy_part,
        #                         **{attr: CategoricalParameter(CandleTrendType)}
        #                     )
        #                     for _ in range(nums)
        #                 ]
        #             )

        #     return replacements

        # def period_invariants(strategy_part):
        #     replacements = []
        #     period_replacement_ranges = [
        #         (
        #             "period",
        #             [
        #                 (RandomParameter(6.0, 20.0, 5.0), 8),
        #                 (RandomParameter(25.0, 50.0, 8.0), 6),
        #                 (RandomParameter(58.0, 100.0, 10.0), 3),
        #             ],
        #         ),
        #         ("atr_period", [(RandomParameter(0.2, 10.0, 0.1), 5)]),
        #     ]

        #     for attr, replacement_ranges in period_replacement_ranges:
        #         if hasattr(strategy_part, attr):
        #             for range_params, num_replacements in replacement_ranges:
        #                 replacements.extend(
        #                     [
        #                         replace(strategy_part, **{attr: range_params})
        #                         for _ in range(num_replacements)
        #                     ]
        #                 )

        #     return replacements

        # def ma_invariants(strategy_part, nums=3):
        #     replacements = []

        #     if hasattr(strategy_part, "ma"):
        #         replacements.extend(
        #             [
        #                 replace(
        #                     strategy_part, ma=CategoricalParameter(MovingAverageType)
        #                 )
        #                 for _ in range(nums)
        #             ]
        #         )

        #     return replacements

        # def factor_invariants(strategy_part, nums=3):
        #     replacements = []

        #     if hasattr(strategy_part, "factor"):
        #         replacements.extend(
        #             [
        #                 replace(strategy_part, factor=RandomParameter(1.0, 8.0, 0.5))
        #                 for _ in range(nums)
        #             ]
        #         )

        #     return replacements

        # def source_invariants(strategy_part, nums=3):
        #     replacements = []

        #     if hasattr(strategy_part, "source_type"):
        #         replacements.extend(
        #             [
        #                 replace(
        #                     strategy_part, source_type=CategoricalParameter(SourceType)
        #                 )
        #                 for _ in range(nums)
        #             ]
        #         )

        #     return replacements

        # for attr in strategy_attributes:
        #     for strategy in result[:]:
        #         strategy_attr = getattr(strategy, attr)

        #         source_parts = source_invariants(strategy_attr)
        #         for part in source_parts:
        #             result.append(replace(strategy, **{attr: part}))

        #         smoothed_parts = smooth_invariants(strategy_attr)
        #         for part in smoothed_parts:
        #             result.append(replace(strategy, **{attr: part}))

        #         ma_parts = ma_invariants(strategy_attr)
        #         for part in ma_parts:
        #             result.append(replace(strategy, **{attr: part}))

        #         candle_parts = candle_invariants(strategy_attr)
        #         for part in candle_parts:
        #             result.append(replace(strategy, **{attr: part}))

        #         period_parts = period_invariants(strategy_attr)
        #         for part in period_parts:
        #             result.append(replace(strategy, **{attr: part}))

        #         factor_parts = factor_invariants(strategy_attr)
        #         for part in factor_parts:
        #             result.append(replace(strategy, **{attr: part}))

        return result

    def _generate_signal(self, signal: TrendSignalType):
        if signal == TrendSignalType.ZERO_CROSS:
            return np.random.choice(
                [
                    AoZeroCrossSignal(),
                    MacdZeroCrossSignal(),
                    RocZeroCrossSignal(),
                    TsiZeroCrossSignal(),
                    TrixZeroCrossSignal(),
                    QstickZeroCrossSignal(),
                    CcZeroCrossSignal(),
                    BopZeroCrossSignal(),
                    CfoZeroCrossSignal(),
                    MadZeroCrossSignal(),
                ]
            )
        if signal == TrendSignalType.SIGNAL_LINE:
            return np.random.choice(
                [
                    DiSignalLineSignal(),
                    DsoSignalLineSignal(),
                    KstSignalLineSignal(),
                    MacdSignalLineSignal(),
                    QstickSignalLineSignal(),
                    RsiSignalLineSignal(),
                    StochSignalLineSignal(),
                    TrixSignalLineSignal(),
                    TsiSignalLineSignal(),
                ]
            )
        if signal == TrendSignalType.PATTERN:
            return np.random.choice(
                [
                    AoSaucerSignal(),
                    CandlestickTrendSignal(),
                    HighLowSignal(),
                ]
            )
        if signal == TrendSignalType.COLOR_SWITCH:
            return np.random.choice(
                [
                    MacdColorSwitchSignal(),
                ]
            )

        if signal == TrendSignalType.CONTRARIAN:
            return np.random.choice(
                [
                    TiiVSignal(),
                    RsiVSignal(),
                    StochESignal(),
                    RsiDSignal(),
                    RsiCSignal(),
                    RsiNtSignal(),
                    RsiUSignal(),
                    SnatrSignal(),
                    CandlestickReversalSignal(),
                    KchCSignal(),
                    KchASignal(),
                ]
            )
        if signal == TrendSignalType.BB:
            return np.random.choice(
                [
                    MacdBbSignal(),
                    VwapBbSignal(),
                ]
            )
        if signal == TrendSignalType.FLIP:
            return np.random.choice(
                [
                    CeFlipSignal(),
                    SupertrendFlipSignal(),
                ]
            )
        if signal == TrendSignalType.MA:
            return np.random.choice(
                [
                    Ma3CrossSignal(),
                    VwapCrossSignal(),
                    Ma2RsiSignal(),
                    MaTestingGroundSignal(),
                    MaQuadrupleSignal(),
                    MaSurpassSignal(),
                    MaCrossSignal(),
                ]
            )
        if signal == TrendSignalType.BREAKOUT:
            return np.random.choice(
                [
                    DchMa2BreakoutSignal(),
                ]
            )
        if signal == TrendSignalType.LINES_TWO_CROSS:
            return np.random.choice(
                [
                    Dmi2LinesCrossSignal(),
                    Vi2LinesCrossSignal(),
                ]
            )
        if signal == TrendSignalType.NEUTRALITY:
            return np.random.choice(
                [
                    DsoNeutralityCrossSignal(),
                    RsiNautralityCrossSignal(),
                    RsiNautralityPullbackSignal(),
                    RsiNautralityRejectionSignal(),
                    TiiNeutralityCrossSignal(),
                ]
            )
        return np.random.choice(
            [
                RsiNautralityRejectionSignal(),
            ]
        )
