class AwesomeOscillator:
    def __init__(self, ao_short_period=5, ao_long_period=34):
        self.ao_short_period = ao_short_period
        self.ao_long_period = ao_long_period

    def ao(self, data):
        median_price = (data['high'] + data['low']) / 2
        sma_short = median_price.rolling(window=self.ao_short_period).mean()
        sma_long = median_price.rolling(window=self.ao_long_period).mean()
        return sma_short - sma_long