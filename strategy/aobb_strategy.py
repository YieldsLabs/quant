from strategy.abstract_strategy import AbstractStrategy
from ta.overlap.zlma import ZeroLagEMA
from ta.volatility.bbands import BollingerBands
from ta.volume.mfi import MoneyFlowIndex
from ta.momentum.awesome_oscillator import AwesomeOscillator


class AwesomeOscillatorBBStrategy(AbstractStrategy):
    NAME = "AOBB"

    def __init__(self, ao_short_period=5, ao_long_period=34, sma_period=25, stdev_multi=2, slow_sma_period=50, mfi_period=14, oversold=40, overbought=60):
        super().__init__()
        self.ao = AwesomeOscillator(ao_short_period=ao_short_period, ao_long_period=ao_long_period)
        self.bb = BollingerBands(sma_period=sma_period, multiplier=stdev_multi)
        self.sma = ZeroLagEMA(window=slow_sma_period)
        self.mfi = MoneyFlowIndex(period=mfi_period)
        self.mfi_buy_level = oversold
        self.mfi_sell_level = overbought

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['sma'] = self.sma.call(data)
        data['ao'] = self.ao.call(data)
        data['upper_band'], _, data['lower_band'] = self.bb.call(data)
        data['mfi'] = self.mfi.call(data)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < 2:
            return False, False

        data = self._add_indicators(ohlcv)

        buy_signal = self._generate_buy_signal(data)
        sell_signal = self._generate_sell_signal(data)

        return buy_signal, sell_signal

    def exit(self, ohlcv):
        pass

    def _generate_buy_signal(self, data):
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        lower_high_price = second_last_row['close'] < last_row['close']
        higher_low_ao = second_last_row['ao'] > last_row['ao']
        price_touch_lower_band = last_row['close'] <= last_row['lower_band']
        mfi_buy_signal = last_row['mfi'] <= self.mfi_buy_level

        return lower_high_price and higher_low_ao and price_touch_lower_band and mfi_buy_signal

    def _generate_sell_signal(self, data):
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        higher_low_price = second_last_row['close'] > last_row['close']
        lower_high_ao = second_last_row['ao'] < last_row['ao']
        price_touch_upper_band = last_row['close'] >= last_row['upper_band']
        mfi_sell_signal = last_row['mfi'] >= self.mfi_sell_level

        return higher_low_price and lower_high_ao and price_touch_upper_band and mfi_sell_signal
