import pandas as pd
from strategy.AbstractStrategy import AbstractStrategy
from ta.MovingAverageIndicator import MovingAverageIndicator

class SmoothVWMAScalpingContrarian(AbstractStrategy):
    def __init__(self, length1=5, length2=200, length3=20):
        super().__init__()
        self.length1 = length1
        self.length2 = length2
        self.length3 = length3

        self.ma_indicator = MovingAverageIndicator(window=self.length1)
        self.vwma_indicator1 = MovingAverageIndicator(window=self.length1)
        self.vwma_indicator2 = MovingAverageIndicator(window=self.length2)
        self.vwma_indicator3 = MovingAverageIndicator(window=self.length3)
   
    def add_indicators(self, data):
        data = data.copy()
        
        close_sma5 = self.ma_indicator.sma(data['close'])

        data['vwma1'] = self.vwma_indicator1.vwma(close_sma5, data['volume'])
        data['vwma2'] = self.vwma_indicator2.vwma(close_sma5, data['volume'])
        data['vwma3'] = self.vwma_indicator3.vwma(close_sma5, data['volume'])

        return data

    def entry(self, data):
        if len(data) < max(self.length1, self.length2, self.length3) + 1:
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]
        prev_row = data.iloc[-2]

        buy_signal = (
            prev_row['vwma1'] < prev_row['vwma2'] and
            current_row['vwma1'] > current_row['vwma2']
        )

        sell_signal = (
            prev_row['vwma1'] > prev_row['vwma2'] and
            current_row['vwma1'] < current_row['vwma2']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'SmoothVWMAScalpingContrarian'
