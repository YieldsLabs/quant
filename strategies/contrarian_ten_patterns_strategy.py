from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy_management.base_strategy import BaseStrategy
from ta.momentum.stochosc import StochasticOscillator
from ta.patterns.abandoned_baby import AbandonedBaby
from ta.patterns.engulfing import Engulfing
from ta.patterns.extreme_euphoria import ExtremeEuphoria
from ta.patterns.harami_cross import HaramiCross
from ta.patterns.kangaroo_tail import KangarooTail
from ta.patterns.morning_evening_star import MorningEveningStar
from ta.patterns.piercingline_darkcloudcover import PiercingLineDarkCloudCover
from ta.patterns.split_candlestick import SplitCandlestick
from ta.patterns.threewhitesoldiers_threeblackcrows import ThreeWhiteSoldiersThreeBlackCrows
from ta.patterns.tweezer_tops_bottoms import TweezerTopsBottoms
from ta.volatility.bbands import BollingerBands


class ContrarianTenPatterns(BaseStrategy):
    NAME = "CONTRARIANTENPATTERNS"

    def __init__(self, sma_period=20, stdev_multi=2, oversold=20, overbought=80, atr_multi=1.2, risk_reward_ratio=2):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (StochasticOscillator(), ('%K', '%D')),
            (ExtremeEuphoria(), (ExtremeEuphoria.bullish_column(), ExtremeEuphoria.bearish_column())),
            (ThreeWhiteSoldiersThreeBlackCrows(), (ThreeWhiteSoldiersThreeBlackCrows.bullish_column(), ThreeWhiteSoldiersThreeBlackCrows.bearish_column())),
            (PiercingLineDarkCloudCover(), (PiercingLineDarkCloudCover.bullish_column(), PiercingLineDarkCloudCover.bearish_column())),
            (SplitCandlestick(), (SplitCandlestick.bullish_column(), SplitCandlestick.bearish_column())),
            (KangarooTail(), (KangarooTail.bullish_column(), KangarooTail.bearish_column())),
            (HaramiCross(), (HaramiCross.bullish_column(), HaramiCross.bearish_column())),
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column())),
            (MorningEveningStar(), (MorningEveningStar.bullish_column(), MorningEveningStar.bearish_column())),
            (AbandonedBaby(), (AbandonedBaby.bullish_column(), AbandonedBaby.bearish_column())),
            (TweezerTopsBottoms(), (TweezerTopsBottoms.bullish_column(), TweezerTopsBottoms.bearish_column())),
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            ATRStopLossFinder(atr_multi=atr_multi)
        )
        self.oversold = oversold
        self.overbought = overbought

    def _generate_buy_entry(self, data):
        bullish_column = (data[ExtremeEuphoria.bullish_column()]
                          | data[ThreeWhiteSoldiersThreeBlackCrows.bullish_column()]
                          | data[Engulfing.bullish_column()]
                          | data[PiercingLineDarkCloudCover.bullish_column()]
                          | data[MorningEveningStar.bullish_column()]
                          | data[SplitCandlestick.bullish_column()]
                          | data[AbandonedBaby.bullish_column()]
                          | data[HaramiCross.bullish_column()]
                          | data[AbandonedBaby.bullish_column()]
                          | data[TweezerTopsBottoms.bullish_column()])

        close = data['close']
        lower_band = data['lower_band']
        percent_k = data['%K']
        percent_d = data['%D']

        oversold_stoch = (percent_k < self.oversold) & (percent_k.shift(1) < percent_d.shift(1)) & (percent_k > percent_d)
        cross_lower_band = close <= lower_band
        buy_entry = bullish_column & cross_lower_band.shift(1) & (close > lower_band) & oversold_stoch

        return buy_entry

    def _generate_sell_entry(self, data):
        bearish_column = (data[ExtremeEuphoria.bearish_column()]
                          | data[ThreeWhiteSoldiersThreeBlackCrows.bearish_column()]
                          | data[Engulfing.bearish_column()]
                          | data[PiercingLineDarkCloudCover.bearish_column()]
                          | data[MorningEveningStar.bearish_column()]
                          | data[SplitCandlestick.bearish_column()]
                          | data[AbandonedBaby.bearish_column()]
                          | data[HaramiCross.bearish_column()]
                          | data[AbandonedBaby.bearish_column()]
                          | data[TweezerTopsBottoms.bearish_column()])

        close = data['close']
        upper_band = data['upper_band']
        percent_k = data['%K']
        percent_d = data['%D']

        overbought_stoch = (percent_k > self.overbought) & (percent_k.shift(1) > percent_d.shift(1)) & (percent_k < percent_d)
        cross_upper_band = close >= upper_band
        sell_entry = bearish_column & cross_upper_band.shift(1) & (close < upper_band) & overbought_stoch

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
