class FairValueGapIndicator:
    def __init__(self, lookback=15):
        self.lookback = lookback
    
    def fvg(self, data):
        fair_values = data['close']
        fair_value_mean = fair_values.rolling(self.lookback, min_periods=self.lookback).mean()
        fair_value_gap = fair_values - fair_value_mean
        
        fair_value_gap.iloc[:self.lookback] = None
        
        return fair_value_gap
