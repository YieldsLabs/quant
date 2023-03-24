from ta.BBIndicator import BBIndicator
from oscillators.awesome import AwesomeOscillator
from strategy.AbstractStrategy import AbstractStrategy

class AwesomeOscillatorBBStrategy(AbstractStrategy):
    def __init__(self, ao_short_period=5, ao_long_period=34, bb_period=20, bb_std_dev=2):
        super().__init__()
        self.ao = AwesomeOscillator(ao_short_period=ao_short_period, ao_long_period=ao_long_period)
        self.bb = BBIndicator(sma_period=bb_period, multiplier=bb_std_dev)

    def add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['ao'] =  self.ao.ao(data)
        data['upper_band'], data['lower_band'] = self.bb.bb(data)
        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False
        
        data = self.add_indicators(data)

        buy_signal = self._generate_buy_signal(data)
        sell_signal = self._generate_sell_signal(data)

        return buy_signal, sell_signal
    
    def __str__(self) -> str:
        return 'AwesomeOscillatorBBStrategy'

    def _generate_buy_signal(self, data):
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        lower_high_price = second_last_row['close'] < last_row['close']
        higher_low_ao = second_last_row['ao'] > last_row['ao']
        price_touch_lower_band = last_row['close'] <= last_row['lower_band']

        return lower_high_price and higher_low_ao and price_touch_lower_band

    def _generate_sell_signal(self, data):
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        higher_low_price = second_last_row['close'] > last_row['close']
        lower_high_ao = second_last_row['ao'] < last_row['ao']
        price_touch_upper_band = last_row['close'] >= last_row['upper_band']

        return higher_low_price and lower_high_ao and price_touch_upper_band
