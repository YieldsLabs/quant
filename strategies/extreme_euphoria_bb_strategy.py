from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.patterns.extreme_euphoria import ExtremeEuphoria
from ta.volatility.bbands import BollingerBands


class ExtremeEuphoriaBollingerBands(BaseStrategy):
    NAME = "EEBB"

    def __init__(self, sma_period=20, stdev_multi=2, risk_reward_ratio=3):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (ExtremeEuphoria(), (ExtremeEuphoria.bullish_column(), ExtremeEuphoria.bearish_column()))
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            LowHighStopLossFinder()
        )

    def _generate_buy_signal(self, data):
        bullish_column = data[ExtremeEuphoria.bullish_column()]
        close = data['close']
        lower_band = data['lower_band']

        buy_signal = bullish_column & (close <= lower_band)

        return buy_signal

    def _generate_sell_signal(self, data):
        bearish_column = data[ExtremeEuphoria.bearish_column()]
        close = data['close']
        upper_band = data['upper_band']

        sell_signal = bearish_column & (close >= upper_band)

        return sell_signal

    def _generate_buy_exit(self, data):
        close = data['close']
        upper_band = data['upper_band']
        bearish_column = data[ExtremeEuphoria.bearish_column()]
        cross_upper_band = close >= upper_band
        re_enter_band = cross_upper_band.shift(1) & (close < upper_band)

        buy_exit_signal = re_enter_band | bearish_column

        return buy_exit_signal

    def _generate_sell_exit(self, data):
        close = data['close']
        lower_band = data['lower_band']
        bullish_column = data[ExtremeEuphoria.bullish_column()]
        cross_lower_band = close <= lower_band

        re_enter_band = cross_lower_band.shift(1) & (close > lower_band)

        sell_exit_signal = re_enter_band | bullish_column

        return sell_exit_signal
