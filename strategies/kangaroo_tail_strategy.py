from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder
from strategy.base_strategy import BaseStrategy
from ta.overlap.zlma import ZeroLagEMA
from ta.patterns.kangaroo_tail import KangarooTail


class KangarooTailZLMA(BaseStrategy):
    NAME = "KTZLMA"

    def __init__(self, slow_sma_period=100, lookback=200, risk_reward_ratio=1.5):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME),
            (KangarooTail(lookback), (KangarooTail.bullish_column(), KangarooTail.bearish_column()))
        ]
        super().__init__(
            indicators,
            RiskRewardTakeProfitFinder(risk_reward_ratio),
            LowHighStopLossFinder(lookback=lookback)
        )

    def _generate_buy_signal(self, data):
        bullish_column = data[KangarooTail.bullish_column()]
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]

        buy_signal = bullish_column & (close > zlema)

        return buy_signal

    def _generate_sell_signal(self, data):
        bearish_column = data[KangarooTail.bearish_column()]
        close = data['close']
        zlema = data[ZeroLagEMA.NAME]

        sell_signal = bearish_column & (close < zlema)

        return sell_signal
