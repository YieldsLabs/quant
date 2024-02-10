from enum import Enum, auto
from itertools import product
from random import shuffle

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from core.models.strategy import Strategy, StrategyType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.confirm.roc import RocConfirm
from strategy.generator.confirm.rsi import RsiConfirm
from strategy.generator.confirm.stc import StcConfirm
from strategy.generator.confirm.supertrend import SupertrendConfirm
from strategy.generator.signal.macd_bb import MacdBbSignal
from strategy.generator.signal.rsi_supertrend import RsiSupertrendSignal
from strategy.generator.signal.vi_cross import ViCrossSignal
from strategy.generator.signal.vwap_bb import VwapBbSignal

from .baseline.ma import MaBaseLine
from .confirm.dpo import DpoConfirm
from .confirm.dumb import DumbConfirm
from .confirm.eom import EomConfirm
from .exit.ast import AstExit
from .exit.ce import CeExit
from .exit.highlow import HighLowExit
from .exit.ma import MaExit
from .exit.pattern import PatternExit
from .exit.rsi import RsiExit
from .pulse.adx import AdxPulse
from .pulse.braid import BraidPulse
from .pulse.chop import ChopPulse
from .pulse.vo import VoPulse
from .signal.ao_flip import AoFlipSignal
from .signal.ao_saucer import AoSaucerSignal
from .signal.apo_flip import ApoFlipSignal
from .signal.bop_flip import BopFlipSignal
from .signal.cc_flip import CcFlipSignal
from .signal.cfo_flip import CfoFlipSignal
from .signal.dch_two_ma import Dch2MaSignal
from .signal.di_cross import DiCrossSignal
from .signal.di_flip import DiFlipSignal
from .signal.dmi_cross import DmiCrossSignal
from .signal.hl import HighLowSignal
from .signal.kst_cross import KstCrossSignal
from .signal.ma_three_cross import Ma3CrossSignal
from .signal.macd_color_switch import MacdColorSwitchSignal
from .signal.macd_cross import MacdCrossSignal
from .signal.macd_flip import MacdFlipSignal
from .signal.qstick_cross import QstickCrossSignal
from .signal.qstick_flip import QstickFlipSignal
from .signal.quadruple import QuadrupleSignal
from .signal.roc_flip import RocFlipSignal
from .signal.rsi_ma_pullback import RsiMaPullbackSignal
from .signal.rsi_neutrality_cross import RsiNautralityCrossSignal
from .signal.rsi_neutrality_pullback import RsiNautralityPullbackSignal
from .signal.rsi_neutrality_rejection import RsiNautralityRejectionSignal
from .signal.rsi_two_ma import Rsi2MaSignal
from .signal.rsi_v import RsiVSignal
from .signal.snatr import SnatrSignal
from .signal.stc_flip import StcFlipSignal
from .signal.stoch_cross import StochCrossSignal
from .signal.supertrend_flip import SupertrendFlipSignal
from .signal.testing_ground import TestingGroundSignal
from .signal.tii_cross import TiiCrossSignal
from .signal.tii_v import TiiVSignal
from .signal.trend_candle import TrendCandleSignal
from .signal.trix_cross import TrixCrossSignal
from .signal.trix_flip import TrixFlipSignal
from .signal.tsi_cross import TsiCrossSignal
from .signal.tsi_flip import TsiFlipSignal
from .signal.vwap_cross import VwapCrossSignal
from .stop_loss.atr import AtrStopLoss


class TrendSignalType(Enum):
    BB = auto()
    CANDLE = auto()
    CROSS = auto()
    FLIP = auto()
    V = auto()
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
        confirm = np.random.choice(
            [
                DumbConfirm(),
                DpoConfirm(),
                EomConfirm(),
                RocConfirm(),
                RsiConfirm(),
                StcConfirm(),
                SupertrendConfirm(),
            ]
        )
        pulse = np.random.choice([AdxPulse(), BraidPulse(), ChopPulse(), VoPulse()])
        baseline = np.random.choice(
            [
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.ALMA),
                    period=StaticParameter(13.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.EMA),
                    period=StaticParameter(55.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.SMA),
                    period=StaticParameter(100.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.HMA),
                    period=StaticParameter(85.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.KJS),
                    period=StaticParameter(26.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.KJS),
                    period=StaticParameter(50.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.T3),
                    period=StaticParameter(8.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.TMA),
                    period=StaticParameter(20.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.GMA),
                    period=StaticParameter(10.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.KAMA),
                    period=StaticParameter(21.0),
                ),
                MaBaseLine(
                    ma=StaticParameter(MovingAverageType.ZLSMA),
                    period=StaticParameter(32.0),
                ),
                MaBaseLine(
                    ma=CategoricalParameter(MovingAverageType),
                    period=RandomParameter(5.0, 100.0, 2.5),
                ),
            ]
        )
        stop_loss = np.random.choice(
            [AtrStopLoss(multi=RandomParameter(1.4, 1.7, 0.15))]
        )
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
                    MacdFlipSignal(
                        smooth_type=StaticParameter(Smooth.SMA),
                        fast_period=StaticParameter(3.0),
                        slow_period=StaticParameter(10.0),
                        signal_period=StaticParameter(16.0),
                    ),
                    MacdFlipSignal(smooth_type=StaticParameter(Smooth.EMA)),
                    MacdFlipSignal(smooth_type=StaticParameter(Smooth.ZLEMA)),
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
                    MacdBbSignal(smooth_type=StaticParameter(Smooth.EMA)),
                    VwapBbSignal(smooth_type=StaticParameter(Smooth.EMA)),
                ]
            )

        if signal == TrendSignalType.CANDLE:
            return np.random.choice(
                [
                    TrendCandleSignal(),
                ]
            )

        if signal == TrendSignalType.CROSS:
            return np.random.choice(
                [
                    Ma3CrossSignal(
                        short_period=ma_short_period,
                        medium_period=ma_medium_period,
                        long_period=ma_long_period,
                    ),
                    MacdCrossSignal(
                        smooth_type=StaticParameter(Smooth.SMA),
                        fast_period=StaticParameter(3.0),
                        slow_period=StaticParameter(10.0),
                        signal_period=StaticParameter(16.0),
                    ),
                    MacdCrossSignal(smooth_type=StaticParameter(Smooth.EMA)),
                    MacdCrossSignal(smooth_type=StaticParameter(Smooth.ZLEMA)),
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
                    RsiNautralityPullbackSignal(),
                    RsiMaPullbackSignal(),
                ]
            )

        return np.random.choice(
            [
                AoSaucerSignal(),
                MacdColorSwitchSignal(
                    smooth_type=StaticParameter(Smooth.SMA),
                    fast_period=StaticParameter(3.0),
                    slow_period=StaticParameter(10.0),
                    signal_period=StaticParameter(16.0),
                ),
                MacdColorSwitchSignal(smooth_type=StaticParameter(Smooth.EMA)),
                MacdColorSwitchSignal(smooth_type=StaticParameter(Smooth.ZLEMA)),
                SnatrSignal(),
                RsiNautralityRejectionSignal(),
                RsiSupertrendSignal(),
                TestingGroundSignal(period=ma_long_period),
                QuadrupleSignal(),
                HighLowSignal(),
            ]
        )
