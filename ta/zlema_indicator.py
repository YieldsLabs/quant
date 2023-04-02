from ta.ma_indicator import MovingAverageIndicator


class ZeroLagEMAIndicator:
    def __init__(self, window=5):
        self.window = window
        self.ma = MovingAverageIndicator(window=window)

    def zero_lag_ema(self, data, column='close'):
        ema = self.ma.ema(data[column])
        lag = (self.window - 1) // 2
        shifted_series = data[column].shift(-lag)
        zlema = 2 * ema - shifted_series.ewm(span=self.window).mean()
        return zlema
    
    def __str__(self) -> str:
        return f'ZeroLagEMAIndicator(window={self.window})'