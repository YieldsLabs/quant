from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.patterns.extreme_euphoria import ExtremeEuphoria
from ta.volatility.bbands import BollingerBands


class ExtremeEuphoriaBollingerBands(BaseStrategy):
    NAME = "EEBB"

    def __init__(self, sma_period=20, stdev_multi=2, risk_reward_ratio=1.5):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (ExtremeEuphoria(), (ExtremeEuphoria.bullish_column(), ExtremeEuphoria.bearish_column()))
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
            LowHighStopLossFinder()
        )

    def _generate_buy_signal(self, data):
        last_row = data.iloc[-1]
        buy_signal = last_row[ExtremeEuphoria.bullish_column()] and (
            last_row['close'] <= last_row['lower_band'])
        return buy_signal

    def _generate_sell_signal(self, data):
        last_row = data.iloc[-1]
        sell_signal = last_row[ExtremeEuphoria.bearish_column()] and (
            last_row['close'] >= last_row['upper_band'])
        return sell_signal
