import pandas as pd


class HigherHighLowerLowIndicator:
    def __init__(self, left_bars=5, right_bars=5):
        self.left_bars = left_bars
        self.right_bars = right_bars

    def hh_ll(self, ohlcv):
        data = ohlcv.copy()

        data['ph'] = data['high'].rolling(
            window=self.left_bars).max().shift(-self.right_bars)
        data['pl'] = data['low'].rolling(
            window=self.left_bars).min().shift(-self.right_bars)

        data['hl'] = (data['ph'].notna().astype(
            int) - data['pl'].notna().astype(int)).replace(0, pd.NA).fillna(method='ffill')

        data['hh'] = data['ph'].notna() & (data['hl'] == 1)
        data['ll'] = data['pl'].notna() & (data['hl'] == -1)

        return data['hh'], data['ll']
