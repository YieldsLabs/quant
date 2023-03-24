from strategy.AbstractStrategy import AbstractStrategy
from patters.PiercingPattern import PiercingPattern
from oscillators.stochastic import StochasticOscillator

class PiercingStochasticStrategy(AbstractStrategy):
    def __init__(self, stochastic_period=14, k_period=3, lower_barrier=20, upper_barrier=80):
        super().__init__()
        self.st = StochasticOscillator(stochastic_period=stochastic_period, k_period=k_period)
        self.lower_barrier = lower_barrier
        self.upper_barrier = upper_barrier

    def add_indicators(self, data):
        data = data.copy()

        data['bullish_piercing'] = PiercingPattern.bullish(data)
        data['bearish_piercing'] = PiercingPattern.bearish(data)

        data['%K'], data['%D'] = self.st.st(data)

        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]

        buy_signal = (
            current_row['bullish_piercing'] and
            current_row['%K'] < self.lower_barrier
        )
        sell_signal = (
            current_row['bearish_piercing'] and
            current_row['%K'] > self.upper_barrier
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'PiercingStochasticStrategy'
