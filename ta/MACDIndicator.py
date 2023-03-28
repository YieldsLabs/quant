from ta.MovingAverageIndicator import MovingAverageIndicator

class MACDIndicator:
    def __init__(self, short_period=12, long_period=26, signal_period=9):
        self.fast_ema = MovingAverageIndicator(window=short_period)
        self.slow_ema = MovingAverageIndicator(window=long_period)
        self.signal_period = signal_period

    def macd(self, data):
        ema_fast = self.fast_ema.ema(data['close'])
        ema_slow =  self.fast_ema.ema(data['close'])
       
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=self.signal_period, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram

