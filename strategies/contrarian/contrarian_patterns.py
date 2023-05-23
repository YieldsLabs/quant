from risk_management.stop_loss.finders.atr_stop_loss_finder import ATRStopLossFinder
from strategy_management.base_strategy import BaseStrategy
from ta.patterns.abandoned_baby import AbandonedBaby
from ta.patterns.engulfing import Engulfing
from ta.patterns.extreme_euphoria import ExtremeEuphoria
from ta.patterns.harami_cross import HaramiCross
from ta.patterns.kangaroo_tail import KangarooTail
from ta.patterns.morning_evening_star import MorningEveningStar
from ta.patterns.piercingline_darkcloudcover import PiercingLineDarkCloudCover
from ta.patterns.threewhitesoldiers_threeblackcrows import ThreeWhiteSoldiersThreeBlackCrows
from ta.volatility.bbands import BollingerBands
from ta.volume.vo import VolumeOscillator


class ContrarianPatterns(BaseStrategy):
    NAME = "CONTRARIANPATTERNS"

    def __init__(self, sma_period=20, stdev_multi=2, oversold=20, overbought=80, lookback=100, atr_multi=1.5, risk_reward_ratio=2):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (VolumeOscillator(), ('VO')),
            (ExtremeEuphoria(), (ExtremeEuphoria.bullish_column(), ExtremeEuphoria.bearish_column())),
            (ThreeWhiteSoldiersThreeBlackCrows(), (ThreeWhiteSoldiersThreeBlackCrows.bullish_column(), ThreeWhiteSoldiersThreeBlackCrows.bearish_column())),
            (PiercingLineDarkCloudCover(), (PiercingLineDarkCloudCover.bullish_column(), PiercingLineDarkCloudCover.bearish_column())),
            (KangarooTail(), (KangarooTail.bullish_column(), KangarooTail.bearish_column())),
            (AbandonedBaby(), (AbandonedBaby.bullish_column(), AbandonedBaby.bearish_column())),
            (MorningEveningStar(), (MorningEveningStar.bullish_column(), MorningEveningStar.bearish_column())),
            (HaramiCross(), (HaramiCross.bullish_column(), HaramiCross.bearish_column())),
        ]
        super().__init__(
            indicators,
            ATRStopLossFinder(atr_multi=atr_multi),
            risk_reward_ratio=risk_reward_ratio
        )
        self.oversold = oversold
        self.overbought = overbought
        self.lookback = lookback

    def _generate_buy_entry(self, data):
        bullish_column = (data[ExtremeEuphoria.bullish_column()]
                          | data[ThreeWhiteSoldiersThreeBlackCrows.bullish_column()]
                          | data[MorningEveningStar.bullish_column()]
                          | data[KangarooTail.bullish_column()]
                          | data[PiercingLineDarkCloudCover.bullish_column()]
                          | data[AbandonedBaby.bullish_column()]
                          | data[HaramiCross.bullish_column()])

        close = data['close']
        lower_band = data['lower_band']
        vo = data['VO']

        cross_lower_band = close <= lower_band
        buy_entry = bullish_column & cross_lower_band.shift(1) & (close > lower_band) & (vo > 0)

        return buy_entry

    def _generate_sell_entry(self, data):
        bearish_column = (data[ExtremeEuphoria.bearish_column()]
                          | data[ThreeWhiteSoldiersThreeBlackCrows.bearish_column()]
                          | data[MorningEveningStar.bearish_column()]
                          | data[KangarooTail.bearish_column()]
                          | data[PiercingLineDarkCloudCover.bearish_column()]
                          | data[AbandonedBaby.bearish_column()]
                          | data[HaramiCross.bearish_column()])

        close = data['close']
        upper_band = data['upper_band']
        vo = data['VO']

        cross_upper_band = close >= upper_band
        sell_entry = bearish_column & cross_upper_band.shift(1) & (close < upper_band) & (vo < 0)

        return sell_entry

    def _generate_buy_exit(self, data):
        close = data['close']
        upper_band = data['upper_band']

        cross_upper_band = close >= upper_band
        buy_exit_signal = cross_upper_band.shift(1) & (close < upper_band)

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        lower_band = data['lower_band']

        cross_lower_band = close <= lower_band
        sell_exit_signal = cross_lower_band.shift(1) & (close > lower_band)

        return sell_exit_signal
