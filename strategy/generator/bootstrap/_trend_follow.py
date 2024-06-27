from dataclasses import replace
from enum import Enum, auto
from itertools import product
from random import shuffle
from typing import List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import CandleTrendType
from core.models.moving_average import MovingAverageType
from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth, SmoothATR
from core.models.source import SourceType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from strategy.generator.baseline.ma import MaBaseLine
from strategy.generator.confirm.braid import BraidConfirm
from strategy.generator.confirm.cc import CcConfirm
from strategy.generator.confirm.cci import CciConfirm
from strategy.generator.confirm.didi import DidiConfirm
from strategy.generator.confirm.dpo import DpoConfirm
from strategy.generator.confirm.eom import EomConfirm
from strategy.generator.confirm.rsi_signalline import RsiSignalLineConfirm
from strategy.generator.confirm.stc import StcConfirm
from strategy.generator.confirm.wpr import WprConfirm
from strategy.generator.exit.highlow import HighLowExit
from strategy.generator.exit.rex import RexExit
from strategy.generator.exit.trix import TrixExit
from strategy.generator.pulse.adx import AdxPulse
from strategy.generator.pulse.chop import ChopPulse
from strategy.generator.pulse.nvol import NvolPulse
from strategy.generator.pulse.sqz import SqzPulse
from strategy.generator.pulse.tdfi import TdfiPulse
from strategy.generator.pulse.vo import VoPulse
from strategy.generator.pulse.wae import WaePulse
from strategy.generator.pulse.yz import YzPulse
from strategy.generator.signal.bb.vwap import VwapBbSignal
from strategy.generator.signal.colorswitch.macd import MacdColorSwitchSignal
from strategy.generator.signal.flip.ce import CeFlipSignal
from strategy.generator.signal.flip.supertrend import SupertrendFlipSignal
from strategy.generator.signal.neutrality.rsi_cross import RsiNautralityCrossSignal
from strategy.generator.signal.neutrality.rsi_rejection import (
    RsiNautralityRejectionSignal,
)
from strategy.generator.signal.pattern.hl import HighLowSignal
from strategy.generator.signal.zerocross.bop import BopZeroCrossSignal
from strategy.generator.signal.zerocross.qstick import QstickZeroCrossSignal
from strategy.generator.stop_loss.atr import AtrStopLoss
from strategy.generator.stop_loss.dch import DchStopLoss


class TrendSignalType(Enum):
    ZERO_CROSS = auto()
    # SIGNAL_LINE = auto()
    # LINES_TWO_CROSS = auto()
    # CONTRARIAN = auto()
    BB = auto()
    # PATTERN = auto()
    COLOR_SWITCH = auto()
    # FLIP = auto()
    # MA = auto()
    # BREAKOUT = auto()
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
        return [
            Strategy(
                *(
                    SupertrendFlipSignal(smooth_atr=StaticParameter(SmoothATR.EMA)),
                    EomConfirm(),
                    StcConfirm(),
                    ChopPulse(smooth_atr=StaticParameter(SmoothATR.EMA)),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.TRIMA),
                        period=StaticParameter(10.0),
                    ),
                    AtrStopLoss(smooth=StaticParameter(SmoothATR.EMA)),
                    HighLowExit(),
                )
            ),
            Strategy(
                *(
                    CeFlipSignal(),
                    EomConfirm(),
                    StcConfirm(),
                    SqzPulse(source=StaticParameter(SourceType.HL2)),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.ZLTEMA),
                        period=StaticParameter(15.0),
                    ),
                    DchStopLoss(),
                    HighLowExit(),
                )
            ),
            Strategy(
                *(
                    VwapBbSignal(),
                    EomConfirm(),
                    DidiConfirm(),
                    WaePulse(),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.TRIMA),
                        period=StaticParameter(10.0),
                    ),
                    AtrStopLoss(smooth=StaticParameter(SmoothATR.EMA)),
                    TrixExit(),
                )
            ),
            Strategy(
                *(
                    HighLowSignal(),
                    RsiSignalLineConfirm(),
                    DidiConfirm(),
                    YzPulse(),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.CAMA),
                        period=StaticParameter(10.0),
                    ),
                    AtrStopLoss(smooth=StaticParameter(SmoothATR.EMA)),
                    HighLowExit(),
                )
            ),
            Strategy(
                *(
                    MacdColorSwitchSignal(),
                    CcConfirm(),
                    StcConfirm(),
                    WaePulse(),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.TEMA),
                        period=StaticParameter(10.0),
                    ),
                    AtrStopLoss(smooth=StaticParameter(SmoothATR.SMMA)),
                    TrixExit(),
                )
            ),
            Strategy(
                *(
                    RsiNautralityCrossSignal(),
                    EomConfirm(),
                    WprConfirm(),
                    SqzPulse(),
                    MaBaseLine(
                        ma=StaticParameter(MovingAverageType.VIDYA),
                        period=StaticParameter(15.0),
                    ),
                    DchStopLoss(),
                    HighLowExit(),
                )
            ),
        ]

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
        primary_confirm = np.random.choice(
            [
                DpoConfirm(),
                EomConfirm(),
                RsiSignalLineConfirm(),
                CcConfirm(),
            ]
        )
        secondary_confirm = np.random.choice(
            [
                CciConfirm(),
                StcConfirm(),
                DidiConfirm(),
                BraidConfirm(),
                WprConfirm(),
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
            ]
        )
        stop_loss = np.random.choice([AtrStopLoss(), DchStopLoss()])
        exit_signal = np.random.choice(
            [
                HighLowExit(),
                TrixExit(),
                RexExit(),
            ]
        )

        return Strategy(
            *(
                entry_signal,
                primary_confirm,
                secondary_confirm,
                pulse,
                baseline,
                stop_loss,
                exit_signal,
            )
        )

    def _generate_invariants(self, base_strategy: Strategy) -> List[Strategy]:
        result = [base_strategy]
        strategy_attributes = []

        def smooth_invariants(strategy_part, nums=8):
            smooth_attr = ["smooth_type", "smooth_signal", "smooth_bb"]
            replacements = []

            for attr in smooth_attr:
                if hasattr(strategy_part, attr):
                    replacements.extend(
                        [
                            replace(
                                strategy_part, **{attr: CategoricalParameter(Smooth)}
                            )
                            for _ in range(nums)
                        ]
                    )

            return replacements

        def candle_invariants(strategy_part, nums=3):
            smooth_attr = ["candle"]
            replacements = []

            for attr in smooth_attr:
                if hasattr(strategy_part, attr):
                    replacements.extend(
                        [
                            replace(
                                strategy_part,
                                **{attr: CategoricalParameter(CandleTrendType)}
                            )
                            for _ in range(nums)
                        ]
                    )

            return replacements

        def period_invariants(strategy_part):
            replacements = []
            period_replacement_ranges = [
                (
                    "period",
                    [
                        (RandomParameter(6.0, 20.0, 5.0), 8),
                        (RandomParameter(25.0, 50.0, 8.0), 6),
                        (RandomParameter(58.0, 100.0, 10.0), 3),
                    ],
                ),
                ("atr_period", [(RandomParameter(0.2, 10.0, 0.1), 5)]),
            ]

            for attr, replacement_ranges in period_replacement_ranges:
                if hasattr(strategy_part, attr):
                    for range_params, num_replacements in replacement_ranges:
                        replacements.extend(
                            [
                                replace(strategy_part, **{attr: range_params})
                                for _ in range(num_replacements)
                            ]
                        )

            return replacements

        def ma_invariants(strategy_part, nums=3):
            replacements = []

            if hasattr(strategy_part, "ma"):
                replacements.extend(
                    [
                        replace(
                            strategy_part, ma=CategoricalParameter(MovingAverageType)
                        )
                        for _ in range(nums)
                    ]
                )

            return replacements

        def factor_invariants(strategy_part, nums=3):
            replacements = []

            if hasattr(strategy_part, "factor"):
                replacements.extend(
                    [
                        replace(strategy_part, factor=RandomParameter(1.0, 8.0, 0.5))
                        for _ in range(nums)
                    ]
                )

            return replacements

        def source_invariants(strategy_part, nums=3):
            replacements = []

            if hasattr(strategy_part, "source_type"):
                replacements.extend(
                    [
                        replace(
                            strategy_part, source_type=CategoricalParameter(SourceType)
                        )
                        for _ in range(nums)
                    ]
                )

            return replacements

        for attr in strategy_attributes:
            for strategy in result[:]:
                strategy_attr = getattr(strategy, attr)

                source_parts = source_invariants(strategy_attr)
                for part in source_parts:
                    result.append(replace(strategy, **{attr: part}))

                # smoothed_parts = smooth_invariants(strategy_attr)
                # for part in smoothed_parts:
                #     result.append(replace(strategy, **{attr: part}))

                # ma_parts = ma_invariants(strategy_attr)
                # for part in ma_parts:
                #     result.append(replace(strategy, **{attr: part}))

                # candle_parts = candle_invariants(strategy_attr)
                # for part in candle_parts:
                #     result.append(replace(strategy, **{attr: part}))

                # period_parts = period_invariants(strategy_attr)
                # for part in period_parts:
                #     result.append(replace(strategy, **{attr: part}))

                # factor_parts = factor_invariants(strategy_attr)
                # for part in factor_parts:
                #     result.append(replace(strategy, **{attr: part}))

        return result

    def _generate_signal(self, signal: TrendSignalType):
        if signal == TrendSignalType.ZERO_CROSS:
            return np.random.choice(
                [
                    # AoZeroCrossSignal(),
                    # MacdZeroCrossSignal(),
                    # RocZeroCrossSignal(),
                    # TsiZeroCrossSignal(),
                    # TrixZeroCrossSignal(),
                    QstickZeroCrossSignal(),
                    # CcZeroCrossSignal(),
                    BopZeroCrossSignal(),
                    # CfoZeroCrossSignal(),
                ]
            )
        # if signal == TrendSignalType.SIGNAL_LINE:
        #     return np.random.choice(
        #         [
        #             # DiSignalLineSignal(),
        #             # DsoSignalLineSignal(),
        #             # KstSignalLineSignal(),
        #             # MacdSignalLineSignal(),
        #             # QstickSignalLineSignal(),
        #             # RsiSignalLineSignal(),
        #             # StochSignalLineSignal(),
        #             # TrixSignalLineSignal(),
        #             # TsiSignalLineSignal(),
        #         ]
        # )
        # if signal == TrendSignalType.PATTERN:
        #     return np.random.choice(
        #         [
        #             # AoSaucerSignal(),
        #             CandlestickTrendSignal(),
        #             HighLowSignal(),
        #         ]
        #     )
        if signal == TrendSignalType.COLOR_SWITCH:
            return np.random.choice(
                [
                    MacdColorSwitchSignal(),
                ]
            )
        # if signal == TrendSignalType.CONTRARIAN:
        #     return np.random.choice(
        #         [
        #             # TiiVSignal(),
        #             # RsiVSignal(),
        #             SnatrSignal(),
        #         ]
        #     )
        if signal == TrendSignalType.BB:
            return np.random.choice(
                [
                    # MacdBbSignal(),
                    VwapBbSignal(),
                ]
            )
        # if signal == TrendSignalType.FLIP:
        #     return np.random.choice(
        #         [
        #             CeFlipSignal(),
        #             SupertrendFlipSignal(),
        #         ]
        #     )
        # if signal == TrendSignalType.MA:
        #     return np.random.choice(
        #         [
        #             # Ma3CrossSignal(),
        #             # VwapCrossSignal(),
        #             # Ma2RsiSignal(),
        #             # MaTestingGroundSignal(),
        #             # MaQuadrupleSignal(),
        #             # MaSurpassSignal(),
        #             MaCrossSignal(),
        #         ]
        #     )
        # if signal == TrendSignalType.BREAKOUT:
        #     return np.random.choice(
        #         [
        #             DchMa2BreakoutSignal(),
        #         ]
        #     )
        # if signal == TrendSignalType.LINES_TWO_CROSS:
        #     return np.random.choice(
        #         [
        #             Dmi2LinesCrossSignal(),
        #             Vi2LinesCrossSignal(),
        #         ]
        #     )
        if signal == TrendSignalType.NEUTRALITY:
            return np.random.choice(
                [
                    # DsoNeutralityCrossSignal(),
                    RsiNautralityCrossSignal(),
                    # RsiNautralityPullbackSignal(),
                    # RsiNautralityRejectionSignal(),
                    # TiiNeutralityCrossSignal(),
                ]
            )
        return np.random.choice(
            [
                RsiNautralityRejectionSignal(),
                # MacdZeroCrossSignal(),
            ]
        )
