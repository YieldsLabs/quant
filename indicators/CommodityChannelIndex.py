from ta.MovingAverageIndicator import MovingAverageIndicator

class CommodityChannelIndex:
    def __init__(self, window=20, method="SMA", smoothing_window=5):
        self.ma = MovingAverageIndicator(window)
        self.method = method
        self.smoothing_window = smoothing_window
        self.cci_window = window

    def hlc3(self, data):
        return (data['high'] + data['low'] + data['close']) / 3

    def moving_average(self, data, method):
        if method == "SMA":
            return self.ma.sma(data)
        elif method == "EMA":
            return self.ma.ema(data)
        elif method == "SMMA (RMA)":
            return self.ma.smma(data)
        elif method == "WMA":
            return self.ma.wma(data)
        elif method == "VWMA":
            return self.ma.vwma(data)

    def cci(self, data):
        src = self.hlc3(data)
        ma = self.moving_average(src, self.method)
        dev = src.rolling(window= self.cci_window).std()
        cci = (src - ma) / (0.015 * dev)
        return cci
