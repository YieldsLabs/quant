import itertools
from enum import Enum, auto
from random import shuffle
from typing import Iterator, List

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.individual import Individual
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
from factor.stop_loss.dch import DchStopLoss


class FactorType(Enum):
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


class PopulationGenerator(AbstractStrategyGenerator):
    def __init__(
        self, symbols: List[Symbol], timeframes: List[Timeframe], n_samples: int
    ):
        super().__init__()
        self.symbols = symbols
        self.timeframes = timeframes
        self.n_samples = n_samples
        self.iter = self._init()

    def signal(self, factor: FactorType):
        factors = {
            FactorType.ZERO_CROSS: [
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
            ],
            FactorType.SIGNAL_LINE: [
                DiSignalLineSignal(),
                DsoSignalLineSignal(),
                KstSignalLineSignal(),
                MacdSignalLineSignal(),
                QstickSignalLineSignal(),
                RsiSignalLineSignal(),
                StochSignalLineSignal(),
                TrixSignalLineSignal(),
                TsiSignalLineSignal(),
            ],
            FactorType.PATTERN: [
                AoSaucerSignal(),
                CandlestickTrendSignal(),
                HighLowSignal(),
            ],
            FactorType.COLOR_SWITCH: [
                MacdColorSwitchSignal(),
            ],
            FactorType.CONTRARIAN: [
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
            ],
            FactorType.BB: [
                MacdBbSignal(),
                VwapBbSignal(),
            ],
            FactorType.FLIP: [
                CeFlipSignal(),
                SupertrendFlipSignal(),
            ],
            FactorType.MA: [
                Ma3CrossSignal(),
                VwapCrossSignal(),
                Ma2RsiSignal(),
                MaTestingGroundSignal(),
                MaQuadrupleSignal(),
                MaSurpassSignal(),
                MaCrossSignal(),
            ],
            FactorType.BREAKOUT: [
                DchMa2BreakoutSignal(),
            ],
            FactorType.LINES_TWO_CROSS: [
                Dmi2LinesCrossSignal(),
                Vi2LinesCrossSignal(),
            ],
            FactorType.NEUTRALITY: [
                DsoNeutralityCrossSignal(),
                RsiNeutralityCrossSignal(),
                RsiNeutralityPullbackSignal(),
                RsiNeutralityRejectionSignal(),
                TiiNeutralityCrossSignal(),
            ],
        }

        return factors.get(factor)

    def baseline(self):
        return [MaBaseLine()]

    def confirm(self):
        return [
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

    def pulse(self):
        return [
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

    def exit(self):
        return [
            HighLowExit(),
            TrixExit(),
            RexExit(),
            MadExit(),
        ]

    def stop_loss(self):
        return [DchStopLoss(), AtrStopLoss()]

    def __iter__(self):
        return self

    def __next__(self) -> Individual:
        try:
            symbol, timeframe, strategy = next(self.iter)
            return Individual(symbol, timeframe, strategy)
        except StopIteration:
            raise StopIteration from None

    def _init(self) -> Iterator:
        sampled_symbols = self._generate_symbols()
        sampled_timeframes = self._generate_timeframes()
        strategies = self._generate_strategies()

        data = list(itertools.product(sampled_symbols, sampled_timeframes, strategies))

        shuffle(data)

        return iter(data)

    def _generate_strategies(self) -> list[Strategy]:
        stratified = self._stratified_strategies()
        random_fill = self._random_strategies(self.n_samples - len(stratified))
        return stratified + random_fill

    def _generate_symbols(self) -> list[Symbol]:
        return np.random.choice(
            self.symbols, size=min(self.n_samples, len(self.symbols)), replace=False
        )

    def _generate_timeframes(self) -> list[Timeframe]:
        return np.random.choice(
            self.timeframes,
            size=min(self.n_samples, len(self.timeframes)),
            replace=False,
        )

    def _stratified_strategies(self):
        strategies = []

        for factor in FactorType:
            signals = self.signal(factor)

            for signal in signals:
                strategies.append(
                    Strategy(
                        signal=signal,
                        confirm=np.random.choice(self.confirm()),
                        pulse=np.random.choice(self.pulse()),
                        baseline=np.random.choice(self.baseline()),
                        stop_loss=np.random.choice(self.stop_loss()),
                        exit=np.random.choice(self.exit()),
                    )
                )
            if len(strategies) >= self.n_samples:
                return strategies

        return strategies

    def _random_strategies(self, count):
        strategies = []

        signals = [self.signal(factor) for factor in FactorType]

        for _ in range(count):
            strategies.append(
                Strategy(
                    signal=np.random.choice(signals),
                    confirm=np.random.choice(self.confirm()),
                    pulse=np.random.choice(self.pulse()),
                    baseline=np.random.choice(self.baseline()),
                    stop_loss=np.random.choice(self.stop_loss()),
                    exit=np.random.choice(self.exit()),
                )
            )

        return strategies
