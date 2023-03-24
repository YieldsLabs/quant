import pandas as pd
from ta.MovingAverageIndicator import MovingAverageIndicator
from ta.ATRIndicator import ATRIndicator

class KeltnerChannelsIndicator:
    def __init__(self, ema_period=20, atr_period=14, multiplier=2):
        self.ema = MovingAverageIndicator(window=ema_period)
        self.atr = ATRIndicator(atr_period)
        self.multiplier = multiplier

    def keltner_channels(self, data):
        data = data.copy()
        ema = self.ema.ema(data['close'])
        atr = self.atr.atr(data)
        upper_band = ema + (atr * self.multiplier)
        lower_band = ema - (atr * self.multiplier)
        
        return upper_band, ema, lower_band
