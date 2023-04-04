from ta.indicators.base.abstract_indicator import AbstractIndicator
from ta.indicators.base.ma import MovingAverage


class FairValueGapIndicator(AbstractIndicator):
    def __init__(self, lookback=15):
        self.lookback = lookback
        self.ma = MovingAverage(window=lookback)
    
    def call(self, data):
        fair_values = data['close']
        
        fair_value_mean = self.ma.sma(fair_values)
        fair_value_gap = fair_values - fair_value_mean
        
        fair_value_gap.iloc[:self.lookback] = None
        
        return fair_value_gap
