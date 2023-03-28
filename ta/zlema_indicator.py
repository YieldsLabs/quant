from ta.ma_indicator import MovingAverageIndicator


class ZeroLagEMAIndicator:
    def __init__(self, window=5):
        self.window = window
        self.ma = MovingAverageIndicator(window=window)

    def zero_lag_ema(self, series):
        ema = self.ma.ema(series)
        lag = (self.window - 1) // 2
        shifted_series = series.shift(-lag)
        zlema = 2 * ema - shifted_series.ewm(span=self.window).mean()
        return zlema