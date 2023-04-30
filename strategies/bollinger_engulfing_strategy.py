from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.patterns.engulfing import Engulfing
from ta.volatility.bbands import BollingerBands


class BollingerBandsEngulfing(BaseStrategy):
    NAME = "BBE"

    def __init__(self, sma_period=20, stdev_multi=2, risk_reward_ratio=1.5):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column()))
        ]

        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            LowHighStopLossFinder()
        )

    def _generate_buy_signal(self, data):
        close = data['close']
        lower_band = data['lower_band']
        bullish_column = data[Engulfing.bullish_column()]

        buy_signal = (close <= lower_band) & bullish_column

        return buy_signal

    def _generate_sell_signal(self, data):
        close = data['close']
        upper_band = data['upper_band']
        bearish_column = data[Engulfing.bearish_column()]

        sell_signal = (close >= upper_band) & bearish_column

        return sell_signal

    def _generate_buy_exit(self, data):
        close = data['close']
        middle_band = data['middle_band']
        bearish_column = data[Engulfing.bearish_column()]

        buy_exit_signal = (close >= middle_band) & bearish_column

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        middle_band = data['middle_band']
        bullish_column = data[Engulfing.bullish_column()]

        sell_exit_signal = (close <= middle_band) & bullish_column

        return sell_exit_signal
