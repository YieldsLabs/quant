import pandas as pd

class ATRIndicator:
    def __init__(self, period=14):
        self.period = period

    def atr(self, data):
        data = data.copy()
        data['previous_close'] = data['close'].shift(1)

        true_range = pd.DataFrame()
        true_range['high_low'] = data['high'] - data['low']
        true_range['high_previous_close'] = abs(data['high'] - data['previous_close'])
        true_range['low_previous_close'] = abs(data['low'] - data['previous_close'])

        data['true_range'] = true_range.max(axis=1)
        data['atr'] = data['true_range'].rolling(window=self.period).mean()
        return data['atr']