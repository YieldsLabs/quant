from strategy.AbstractStrategy import AbstractStrategy
from ta.RSIIndicator import RSIIndicator
from ta.VAMAIndicator import VAMAIndicator

class RSI_VAMAStrategy(AbstractStrategy):
    def __init__(self, rsi_period=14, short_volatility=50, long_volatility=1000, alpha_factor=0.20):
        super().__init__()
        self.rsi_indicator = RSIIndicator(rsi_period)
        self.vama_indicator = VAMAIndicator(short_volatility, long_volatility, alpha_factor)

    def add_indicators(self, data):
        data = data.copy()
        data['rsi'] = self.rsi_indicator.rsi(data['close'])
        data['vama'] = self.vama_indicator.vama(data)
        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)

        last_row = data.iloc[-1]
        prev_row = data.iloc[-2]

        buy_signal = (
            last_row['rsi'] > 50
            and last_row['close'] < last_row['vama']
            and prev_row['close'] > prev_row['vama']
        )

        sell_signal = (
            last_row['rsi'] < 50
            and last_row['close'] > last_row['vama']
            and prev_row['close'] < prev_row['vama']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'RSI_VAMAStrategy'
