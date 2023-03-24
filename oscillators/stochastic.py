class StochasticOscillator:
    def __init__(self, stochastic_period=14, k_period=3):
        self.stochastic_period = stochastic_period
        self.k_period = k_period

    def st(self, data):
        high_low_range = data['high'].rolling(
            window=self.stochastic_period).max() - data['low'].rolling(window=14).min()
        close_low_range = data['close'] - \
            data['low'].rolling(window=self.stochastic_period).min()
        percent_k = (close_low_range / high_low_range) * 100
        percent_d = percent_k.rolling(window=self.k_period).mean()
        return percent_k, percent_d
