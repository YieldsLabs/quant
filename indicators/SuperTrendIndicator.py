import pandas as pd
import numpy as np
from ta.ATRIndicator import ATRIndicator

class SuperTrendIndicator:
    def __init__(self, atr_period=14, multiplier=3):
        self.atr_indicator = ATRIndicator(atr_period)
        self.multiplier = multiplier

    def supertrend(self, data):
        atr = self.atr_indicator.atr(data)
        hl2 = (data['high'] + data['low']) / 2
        upper_band = hl2 + (atr * self.multiplier)
        lower_band = hl2 - (atr * self.multiplier)

        supertrend = pd.Series(np.nan, index=data.index)

        for i in range(atr.size, len(data)):
            if data['close'][i] > upper_band[i - 1]:
                supertrend[i] = lower_band[i]
            elif data['close'][i] < lower_band[i - 1]:
                supertrend[i] = upper_band[i]
            else:
                supertrend[i] = supertrend[i - 1]

                if (supertrend[i - 1] == upper_band[i - 1]) and (data['close'][i] <= upper_band[i]):
                    supertrend[i] = upper_band[i]
                elif (supertrend[i - 1] == lower_band[i - 1]) and (data['close'][i] >= lower_band[i]):
                    supertrend[i] = lower_band[i]

        return supertrend