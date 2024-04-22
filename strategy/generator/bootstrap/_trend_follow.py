from dataclasses import replace
from enum import Enum, auto
from itertools import product
from random import shuffle
from typing import List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import CandleTrendType
from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter
from core.models.smooth import Smooth
from core.models.strategy import Strategy, StrategyType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.baseline.ma import MaBaseLine
from strategy.generator.confirm.cci import CciConfirm
from strategy.generator.confirm.dpo import DpoConfirm
from strategy.generator.confirm.dso import DsoConfirm
from strategy.generator.confirm.eom import EomConfirm
from strategy.generator.confirm.roc import RocConfirm
from strategy.generator.confirm.rsi_neutrality import RsiNeutralityConfirm
from strategy.generator.confirm.rsi_signalline import RsiSignalLineConfirm
from strategy.generator.confirm.stc import StcConfirm
from strategy.generator.confirm.vi import ViConfirm
from strategy.generator.exit.cci import CciExit
from strategy.generator.exit.highlow import HighLowExit
from strategy.generator.exit.ma import MaExit
from strategy.generator.exit.mfi import MfiExit
from strategy.generator.exit.rsi import RsiExit
from strategy.generator.exit.trix import TrixExit
from strategy.generator.pulse.adx import AdxPulse
from strategy.generator.pulse.braid import BraidPulse
from strategy.generator.pulse.chop import ChopPulse
from strategy.generator.pulse.nvol import NvolPulse
from strategy.generator.pulse.tdfi import TdfiPulse
from strategy.generator.pulse.vo import VoPulse
from strategy.generator.pulse.wae import WaePulse
from strategy.generator.signal.bb.macd_bb import MacdBbSignal
from strategy.generator.signal.bb.vwap_bb import VwapBbSignal
from strategy.generator.signal.breakout.dch_two_ma import DchMa2BreakoutSignal
from strategy.generator.signal.flip.supertrend_flip import SupertrendFlipSignal
from strategy.generator.signal.ma.ma2_rsi import Ma2RsiSignal
from strategy.generator.signal.ma.ma3_cross import Ma3CrossSignal
from strategy.generator.signal.ma.ma_cross import MaCrossSignal
from strategy.generator.signal.ma.ma_testing_ground import MaTestingGroundSignal
from strategy.generator.signal.ma.vwap_cross import VwapCrossSignal
from strategy.generator.signal.neutrality.dso_neutrality_cross import (
    DsoNeutralityCrossSignal,
)
from strategy.generator.signal.neutrality.rsi_neutrality_cross import (
    RsiNautralityCrossSignal,
)
from strategy.generator.signal.neutrality.rsi_neutrality_pullback import (
    RsiNautralityPullbackSignal,
)
from strategy.generator.signal.neutrality.rsi_neutrality_rejection import (
    RsiNautralityRejectionSignal,
)
from strategy.generator.signal.neutrality.tii_neutrality_cross import (
    TiiNeutralityCrossSignal,
)
from strategy.generator.signal.pattern.ao_saucer import AoSaucerSignal
from strategy.generator.signal.pattern.candle_trend import CandlestickTrendSignal
from strategy.generator.signal.pattern.hl import HighLowSignal
from strategy.generator.signal.pattern.macd_colorswitch import MacdColorSwitchSignal
from strategy.generator.signal.pattern.rsi_v import RsiVSignal
from strategy.generator.signal.pattern.tii_v import TiiVSignal
from strategy.generator.signal.reversal.dmi_reversal import DmiReversalSignal
from strategy.generator.signal.reversal.snatr_reversal import SnatrReversalSignal
from strategy.generator.signal.reversal.vi_reversal import ViReversalSignal
from strategy.generator.signal.signalline.di_signalline import DiSignalLineSignal
from strategy.generator.signal.signalline.dso_signalline import DsoSignalLineSignal
from strategy.generator.signal.signalline.kst_signalline import KstSignalLineSignal
from strategy.generator.signal.signalline.macd_signalline import MacdSignalLineSignal
from strategy.generator.signal.signalline.qstick_signalline import (
    QstickSignalLineSignal,
)
from strategy.generator.signal.signalline.rsi_signalline import RsiSignalLineSignal
from strategy.generator.signal.signalline.stoch_signalline import StochSignalLineSignal
from strategy.generator.signal.signalline.trix_signalline import TrixSignalLineSignal
from strategy.generator.signal.signalline.tsi_signalline import TsiSignalLineSignal
from strategy.generator.signal.zerocross.ao_zerocross import AoZeroCrossSignal
from strategy.generator.signal.zerocross.apo_zerocross import ApoZeroCrossSignal
from strategy.generator.signal.zerocross.bop_zerocross import BopZeroCrossSignal
from strategy.generator.signal.zerocross.cc_zerocross import CcZeroCrossSignal
from strategy.generator.signal.zerocross.cfo_zerocross import CfoZeroCrossSignal
from strategy.generator.signal.zerocross.macd_zerocross import MacdZeroCrossSignal
from strategy.generator.signal.zerocross.qstick_zerocross import QstickZeroCrossSignal
from strategy.generator.signal.zerocross.roc_zerocross import RocZeroCrossSignal
from strategy.generator.signal.zerocross.trix_zerocross import TrixZeroCrossSignal
from strategy.generator.signal.zerocross.tsi_zerocross import TsiZeroCrossSignal
from strategy.generator.stop_loss.atr import AtrStopLoss
from strategy.generator.stop_loss.dch import DchStopLoss


class TrendSignalType(Enum):
    ZERO_CROSS = auto()
    SIGNAL_LINE = auto()
    BB = auto()
    PATTERN = auto()
    FLIP = auto()
    MA = auto()
    BREAKOUT = auto()
    REVERSAL = auto()
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
        baseline = np.random.choice([MaBaseLine()])
        confirm = np.random.choice(
            [
                DpoConfirm(),
                EomConfirm(),
                RocConfirm(),
                RsiSignalLineConfirm(),
                RsiNeutralityConfirm(),
                StcConfirm(),
                DsoConfirm(),
                CciConfirm(),
                ViConfirm(),
            ]
        )
        pulse = np.random.choice(
            [
                AdxPulse(),
                ChopPulse(),
                BraidPulse(),
                VoPulse(),
                NvolPulse(),
                TdfiPulse(),
                WaePulse(),
            ]
        )
        stop_loss = np.random.choice([AtrStopLoss(), DchStopLoss()])
        exit_signal = np.random.choice(
            [
                # AstExit(),
                HighLowExit(),
                MaExit(),
                RsiExit(),
                MfiExit(),
                CciExit(),
                TrixExit(),
            ]
        )

        return Strategy(
            *(
                StrategyType.TREND,
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
        attributes = []

        def smooth_invariants(strategy_part):
            if not hasattr(strategy_part, "smooth_type") or not hasattr(
                strategy_part, "smooth_signal"
            ):
                return []

            return [
                replace(strategy_part, smooth_type=CategoricalParameter(Smooth))
                for _ in range(5)
            ] + [
                replace(strategy_part, smooth_signal=CategoricalParameter(Smooth))
                for _ in range(5)
            ]

        def candle_invariants(strategy_part):
            if not hasattr(strategy_part, "candle"):
                return []

            return [
                replace(strategy_part, candle=CategoricalParameter(CandleTrendType))
                for _ in range(5)
            ]

        def period_invariants(strategy_part):
            if not hasattr(strategy_part, "period"):
                return []

            return (
                [
                    replace(strategy_part, period=RandomParameter(8.0, 20.0, 5.0))
                    for _ in range(2)
                ]
                + [
                    replace(strategy_part, period=RandomParameter(25.0, 50.0, 8.0))
                    for _ in range(3)
                ]
                + [
                    replace(strategy_part, period=RandomParameter(58.0, 100.0, 10.0))
                    for _ in range(2)
                ]
            )

        def ma_invariants(strategy_part):
            if not hasattr(strategy_part, "ma"):
                return []

            return [
                replace(strategy_part, ma=CategoricalParameter(MovingAverageType))
                for _ in range(3)
            ]

        def factor_invariants(strategy_part):
            if not hasattr(strategy_part, "factor"):
                return []

            return [
                replace(strategy_part, factor=RandomParameter(1.0, 8.0, 0.5))
                for _ in range(3)
            ]

        for attr in attributes:
            for strategy in result[:]:
                strategy_attr = getattr(strategy, attr)

                smoothed_parts = smooth_invariants(strategy_attr)
                for part in smoothed_parts:
                    result.append(replace(strategy, **{attr: part}))

                ma_parts = ma_invariants(strategy_attr)
                for part in ma_parts:
                    result.append(replace(strategy, **{attr: part}))

                candle_parts = candle_invariants(strategy_attr)
                for part in candle_parts:
                    result.append(replace(strategy, **{attr: part}))

                factor_parts = factor_invariants(strategy_attr)
                for part in factor_parts:
                    result.append(replace(strategy, **{attr: part}))

                period_parts = period_invariants(strategy_attr)
                for part in period_parts:
                    result.append(replace(strategy, **{attr: part}))

        return result

    def _generate_signal(self, signal: TrendSignalType):
        if signal == TrendSignalType.ZERO_CROSS:
            return np.random.choice(
                [
                    AoZeroCrossSignal(),
                    ApoZeroCrossSignal(),
                    BopZeroCrossSignal(),
                    MacdZeroCrossSignal(),
                    RocZeroCrossSignal(),
                    TsiZeroCrossSignal(),
                    TrixZeroCrossSignal(),
                    QstickZeroCrossSignal(),
                    CcZeroCrossSignal(),
                    BopZeroCrossSignal(),
                    CfoZeroCrossSignal(),
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
                    MacdColorSwitchSignal(),
                    TiiVSignal(),
                    RsiVSignal(),
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
                    # CeFlipSignal(),
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
                    # MaQuadrupleSignal(),
                    # MaSurpassSignal(),
                    MaCrossSignal(),
                ]
            )
        if signal == TrendSignalType.BREAKOUT:
            return np.random.choice(
                [
                    DchMa2BreakoutSignal(),
                ]
            )
        if signal == TrendSignalType.REVERSAL:
            return np.random.choice(
                [
                    DmiReversalSignal(),
                    SnatrReversalSignal(),
                    ViReversalSignal(),
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
                MacdZeroCrossSignal(),
            ]
        )
