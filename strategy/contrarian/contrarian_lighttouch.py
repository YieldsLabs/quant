from risk_management.stop_loss.finders.atr_stop_loss_finder import ATRStopLossFinder
from strategy.base_strategy import BaseStrategy
from ta.overlap.sma import SimpleMA
from ta.volatility.bbands import BollingerBands
from ta.volume.vo import VolumeOscillator


class ContrarianLightTouch(BaseStrategy):
    NAME = "CONTRARIANLIGHTTOUCH"

    def __init__(self, sma_period=20, stdev_multi=2, slow_sma_period=200, atr_multi=1.5, risk_reward_ratio=2):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band')),
            (VolumeOscillator(), ('VO')),
            (SimpleMA(slow_sma_period), ('sma'))
        ]
        super().__init__(
            indicators,
            ATRStopLossFinder(atr_multi=atr_multi),
            risk_reward_ratio=risk_reward_ratio
        )

    def _generate_buy_entry(self, data):
        close = data['close']
        ma = data['sma']
        vo = data['VO']
        low = data['low']
        lower_band = data['lower_band']

        buy_entry = (low < ma) & (close > ma) & (low < lower_band) & (close > lower_band)

        return buy_entry & (vo > 0)

    def _generate_sell_entry(self, data):
        close = data['close']
        ma = data['sma']
        vo = data['VO']
        high = data['high']
        upper_band = data['upper_band']

        sell_entry = (high > ma) & (close < ma) & (high > upper_band) & (close < upper_band)

        return sell_entry & (vo < 0)

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
