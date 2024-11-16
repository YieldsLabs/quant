from enum import Enum, auto
from itertools import product
from random import shuffle
from typing import List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from factor.baseline.ma import MaBaseLine
from factor.confirm.bb import BbConfirm
from factor.confirm.braid import BraidConfirm
from factor.confirm.cc import CcConfirm
from factor.confirm.cci import CciConfirm
from factor.confirm.didi import DidiConfirm
from factor.confirm.dpo import DpoConfirm
from factor.confirm.dumb import DumbConfirm
from factor.confirm.eom import EomConfirm
from factor.confirm.rsi_signalline import RsiSignalLineConfirm
from factor.confirm.stc import StcConfirm
from factor.confirm.wpr import WprConfirm
from factor.exit.highlow import HighLowExit
from factor.exit.mad import MadExit
from factor.exit.rex import RexExit
from factor.exit.trix import TrixExit
from factor.pulse.adx import AdxPulse
from factor.pulse.chop import ChopPulse
from factor.pulse.dumb import DumbPulse
from factor.pulse.nvol import NvolPulse
from factor.pulse.sqz import SqzPulse
from factor.pulse.tdfi import TdfiPulse
from factor.pulse.vo import VoPulse
from factor.pulse.wae import WaePulse
from factor.pulse.yz import YzPulse
from factor.signal.bb.macd import MacdBbSignal
from factor.signal.bb.vwap import VwapBbSignal
from factor.signal.breakout.dch_two_ma import DchMa2BreakoutSignal
from factor.signal.colorswitch.macd import MacdColorSwitchSignal
from factor.signal.contrarian.kch_a import KchASignal
from factor.signal.contrarian.kch_c import KchCSignal
from factor.signal.contrarian.rsi_c import RsiCSignal
from factor.signal.contrarian.rsi_d import RsiDSignal
from factor.signal.contrarian.rsi_nt import RsiNtSignal
from factor.signal.contrarian.rsi_u import RsiUSignal
from factor.signal.contrarian.rsi_v import RsiVSignal
from factor.signal.contrarian.snatr import SnatrSignal
from factor.signal.contrarian.stoch_e import StochESignal
from factor.signal.contrarian.tii_v import TiiVSignal
from factor.signal.flip.ce import CeFlipSignal
from factor.signal.flip.supertrend import SupertrendFlipSignal
from factor.signal.ma.ma2_rsi import Ma2RsiSignal
from factor.signal.ma.ma3_cross import Ma3CrossSignal
from factor.signal.ma.ma_cross import MaCrossSignal
from factor.signal.ma.ma_quadruple import MaQuadrupleSignal
from factor.signal.ma.ma_surpass import MaSurpassSignal
from factor.signal.ma.ma_testing_ground import MaTestingGroundSignal
from factor.signal.ma.vwap_cross import VwapCrossSignal
from factor.signal.neutrality.dso_cross import DsoNeutralityCrossSignal
from factor.signal.neutrality.rsi_cross import RsiNeutralityCrossSignal
from factor.signal.neutrality.rsi_pullback import RsiNeutralityPullbackSignal
from factor.signal.neutrality.rsi_rejection import RsiNeutralityRejectionSignal
from factor.signal.neutrality.tii_cross import TiiNeutralityCrossSignal
from factor.signal.pattern.ao_saucer import AoSaucerSignal
from factor.signal.pattern.candle_reversal import CandlestickReversalSignal
from factor.signal.pattern.candle_trend import CandlestickTrendSignal
from factor.signal.pattern.hl import HighLowSignal
from factor.signal.signalline.di import DiSignalLineSignal
from factor.signal.signalline.dso import DsoSignalLineSignal
from factor.signal.signalline.kst import KstSignalLineSignal
from factor.signal.signalline.macd import MacdSignalLineSignal
from factor.signal.signalline.qstick import QstickSignalLineSignal
from factor.signal.signalline.rsi import RsiSignalLineSignal
from factor.signal.signalline.stoch import StochSignalLineSignal
from factor.signal.signalline.trix import TrixSignalLineSignal
from factor.signal.signalline.tsi import TsiSignalLineSignal
from factor.signal.twolinescross.dmi import Dmi2LinesCrossSignal
from factor.signal.twolinescross.vi import Vi2LinesCrossSignal
from factor.signal.zerocross.ao import AoZeroCrossSignal
from factor.signal.zerocross.bop import BopZeroCrossSignal
from factor.signal.zerocross.cc import CcZeroCrossSignal
from factor.signal.zerocross.cfo import CfoZeroCrossSignal
from factor.signal.zerocross.macd import MacdZeroCrossSignal
from factor.signal.zerocross.mad import MadZeroCrossSignal
from factor.signal.zerocross.qstick import QstickZeroCrossSignal
from factor.signal.zerocross.roc import RocZeroCrossSignal
from factor.signal.zerocross.trix import TrixZeroCrossSignal
from factor.signal.zerocross.tsi import TsiZeroCrossSignal
from factor.stop_loss.atr import AtrStopLoss


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


class StrategyGenerator(AbstractStrategyGenerator):
    def __init__(self, n_samples):
        super().__init__()
        self.n_samples = n_samples

    def generate(self, symbols, timeframes) -> list[tuple[Symbol, Timeframe, Strategy]]:
        sampled_symbols = self._generate_symbols(symbols)
        sampled_timeframes = self._generate_timeframes(timeframes)
        strategies = self._generate_strategies()

        data = list(set(product(sampled_symbols, sampled_timeframes, strategies)))

        shuffle(data)

        return data

    def _generate_strategies(self) -> list[Strategy]:
        return self._diversified_strategies() + self._random_strategies()

    def _generate_symbols(self, symbols) -> list[Symbol]:
        num_symbols_to_sample = min(self.n_samples, len(symbols))

        return np.random.choice(symbols, size=num_symbols_to_sample, replace=False)

    def _generate_timeframes(self, timeframes) -> list[Timeframe]:
        num_timeframes_to_sample = min(self.n_samples, len(timeframes))

        return np.random.choice(
            timeframes, size=num_timeframes_to_sample, replace=False
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
                    RsiNeutralityCrossSignal(),
                    RsiNeutralityPullbackSignal(),
                    RsiNeutralityRejectionSignal(),
                    TiiNeutralityCrossSignal(),
                ]
            )
        return np.random.choice(
            [
                RsiNeutralityRejectionSignal(),
            ]
        )
