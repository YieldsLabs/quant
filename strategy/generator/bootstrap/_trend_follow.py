from dataclasses import replace
from enum import Enum, auto
from itertools import product
from random import shuffle
from typing import List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import TrendCandleType
from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.strategy import Strategy, StrategyType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.baseline.ma import MaBaseLine
from strategy.generator.confirm.braid import BraidConfirm
from strategy.generator.confirm.dpo import DpoConfirm
from strategy.generator.confirm.eom import EomConfirm
from strategy.generator.confirm.roc import RocConfirm
from strategy.generator.confirm.rsi import RsiConfirm
from strategy.generator.confirm.stc import StcConfirm
from strategy.generator.confirm.supertrend import SupertrendConfirm
from strategy.generator.exit.ast import AstExit
from strategy.generator.exit.ce import CeExit
from strategy.generator.exit.highlow import HighLowExit
from strategy.generator.exit.ma import MaExit
from strategy.generator.exit.pattern import PatternExit
from strategy.generator.exit.rsi import RsiExit
from strategy.generator.pulse.adx import AdxPulse
from strategy.generator.pulse.chop import ChopPulse
from strategy.generator.pulse.vo import VoPulse
from strategy.generator.signal.ao_flip import AoFlipSignal
from strategy.generator.signal.ao_saucer import AoSaucerSignal
from strategy.generator.signal.apo_flip import ApoFlipSignal
from strategy.generator.signal.bop_flip import BopFlipSignal
from strategy.generator.signal.cc_flip import CcFlipSignal
from strategy.generator.signal.cfo_flip import CfoFlipSignal
from strategy.generator.signal.dch_two_ma import Dch2MaSignal
from strategy.generator.signal.di_cross import DiCrossSignal
from strategy.generator.signal.di_flip import DiFlipSignal
from strategy.generator.signal.dmi_cross import DmiCrossSignal
from strategy.generator.signal.hl import HighLowSignal
from strategy.generator.signal.kst_cross import KstCrossSignal
from strategy.generator.signal.ma_three_cross import Ma3CrossSignal
from strategy.generator.signal.macd_bb import MacdBbSignal
from strategy.generator.signal.macd_color_switch import MacdColorSwitchSignal
from strategy.generator.signal.macd_cross import MacdCrossSignal
from strategy.generator.signal.macd_flip import MacdFlipSignal
from strategy.generator.signal.qstick_cross import QstickCrossSignal
from strategy.generator.signal.qstick_flip import QstickFlipSignal
from strategy.generator.signal.quadruple import QuadrupleSignal
from strategy.generator.signal.roc_flip import RocFlipSignal
from strategy.generator.signal.rsi_ma_pullback import RsiMaPullbackSignal
from strategy.generator.signal.rsi_neutrality_cross import RsiNautralityCrossSignal
from strategy.generator.signal.rsi_neutrality_pullback import (
    RsiNautralityPullbackSignal,
)
from strategy.generator.signal.rsi_neutrality_rejection import (
    RsiNautralityRejectionSignal,
)
from strategy.generator.signal.rsi_supertrend import RsiSupertrendSignal
from strategy.generator.signal.rsi_two_ma import Rsi2MaSignal
from strategy.generator.signal.rsi_v import RsiVSignal
from strategy.generator.signal.snatr import SnatrSignal
from strategy.generator.signal.stc_flip import StcFlipSignal
from strategy.generator.signal.stoch_cross import StochCrossSignal
from strategy.generator.signal.supertrend_flip import SupertrendFlipSignal
from strategy.generator.signal.testing_ground import TestingGroundSignal
from strategy.generator.signal.tii_cross import TiiCrossSignal
from strategy.generator.signal.tii_v import TiiVSignal
from strategy.generator.signal.trend_candle import TrendCandleSignal
from strategy.generator.signal.trix_cross import TrixCrossSignal
from strategy.generator.signal.trix_flip import TrixFlipSignal
from strategy.generator.signal.tsi_cross import TsiCrossSignal
from strategy.generator.signal.tsi_flip import TsiFlipSignal
from strategy.generator.signal.vi_cross import ViCrossSignal
from strategy.generator.signal.vwap_bb import VwapBbSignal
from strategy.generator.signal.vwap_cross import VwapCrossSignal
from strategy.generator.stop_loss.atr import AtrStopLoss


class TrendSignalType(Enum):
    BB = auto()
    CANDLE = auto()
    CROSS = auto()
    HISTOGRAM = auto()
    HFT = auto()
    FLIP = auto()
    V = auto()
    MA = auto()
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
        sampled_symbols = self.generate_symbols()
        sampled_timeframes = self.generate_timeframes()
        strategies = self.generate_strategies()

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
                BraidConfirm(),
                DpoConfirm(),
                EomConfirm(),
                RocConfirm(),
                RsiConfirm(),
                StcConfirm(),
                SupertrendConfirm(),
            ]
        )
        pulse = np.random.choice([AdxPulse(), ChopPulse(), VoPulse()])
        stop_loss = np.random.choice([AtrStopLoss()])
        exit_signal = np.random.choice(
            [
                AstExit(),
                CeExit(),
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
                confirm,
                pulse,
                baseline,
                stop_loss,
                exit_signal,
            )
        )

    def _generate_invariants(self, base_strategy: Strategy) -> List[Strategy]:
        result = [base_strategy]
        attributes = ["entry", "baseline"]
        smooth_type_map = {
            str(Smooth.EMA): [Smooth.ZLEMA, Smooth.KAMA],
            str(Smooth.SMA): [Smooth.SMMA, Smooth.LSMA],
            str(Smooth.WMA): [Smooth.HMA],
        }

        def smooth_invariants(strategy_part):
            if not hasattr(strategy_part, "smooth_type") or not hasattr(
                strategy_part, "smooth_signal"
            ):
                return []

            smooth_types = smooth_type_map.get(str(strategy_part.smooth_type.value), [])
            smooth_signals = smooth_type_map.get(
                str(strategy_part.smooth_signal.value), []
            )
            return [
                replace(strategy_part, smooth_type=StaticParameter(smooth_type))
                for smooth_type in smooth_types
            ] + [
                replace(strategy_part, smooth_signal=StaticParameter(smooth_signal))
                for smooth_signal in smooth_signals
            ]

        def candle_invariants(strategy_part):
            if not hasattr(strategy_part, "candle"):
                return []

            return [
                replace(strategy_part, candle=CategoricalParameter(TrendCandleType))
                for _ in range(3)
            ]

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
                for _ in range(2)
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

        return result

    def _generate_signal(self, signal: TrendSignalType):
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
        if signal == TrendSignalType.BB:
            return np.random.choice(
                [
                    MacdBbSignal(),
                    VwapBbSignal(),
                ]
            )
        if signal == TrendSignalType.CANDLE:
            return np.random.choice(
                [
                    TrendCandleSignal(),
                ]
            )
        if signal == TrendSignalType.HISTOGRAM:
            return np.random.choice(
                [
                    AoSaucerSignal(),
                    MacdColorSwitchSignal(),
                ]
            )
        if signal == TrendSignalType.HFT:
            return np.random.choice([HighLowSignal()])
        if signal == TrendSignalType.CROSS:
            return np.random.choice(
                [
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
                    ViCrossSignal(),
                ]
            )
        if signal == TrendSignalType.MA:
            return np.random.choice(
                [
                    Ma3CrossSignal(),
                    Rsi2MaSignal(),
                    Dch2MaSignal(),
                    TestingGroundSignal(),
                    QuadrupleSignal(),
                ]
            )
        if signal == TrendSignalType.PULLBACK:
            return np.random.choice(
                [
                    RsiNautralityPullbackSignal(),
                    RsiMaPullbackSignal(),
                ]
            )

        return np.random.choice(
            [
                SnatrSignal(),
                RsiNautralityRejectionSignal(),
                RsiSupertrendSignal(),
            ]
        )
