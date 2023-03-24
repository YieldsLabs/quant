from strategy.AbstractStrategy import AbstractStrategy
from indicators.ParabolicSARIndicator import ParabolicSARIndicator
from indicators.ZeroLagEMAIndicator import ZeroLagEMAIndicator
from indicators.CommodityChannelIndex import CommodityChannelIndex

class PSARZeroLagEMAStrategy(AbstractStrategy):
    def __init__(self, parabolic_start=0.02, parabolic_increment=0.02, parabolic_maximum=0.2, ema_period=20, cci_window=20):
        super().__init__()
        self.psar_indicator = ParabolicSARIndicator(parabolic_start, parabolic_increment, parabolic_maximum)
        self.ema_indicator = ZeroLagEMAIndicator(ema_period)
        self.cci = CommodityChannelIndex(window=cci_window)

    def add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['psar'] = self.psar_indicator.parabolic_sar(data)
        data['zero_lag_ema'] = self.ema_indicator.zero_lag_ema(data)
        data['cci'] = self.cci.cci(data)

        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False
        
        data = self.add_indicators(data)

        buy_signal = self._generate_buy_signal(data)
        sell_signal = self._generate_sell_signal(data)

        return buy_signal, sell_signal
    
    def __str__(self) -> str:
        return 'PSARZeroLagEMAStrategy'

    @staticmethod
    def _generate_buy_signal(data):
        last_row = data.iloc[-1]
        return (
            last_row['close'] > last_row['zero_lag_ema'] and
            last_row['close'] > last_row['psar'] and 
            last_row['cci'] > 100
        )

    @staticmethod
    def _generate_sell_signal(data):
        last_row = data.iloc[-1]
        return (
            last_row['close'] < last_row['zero_lag_ema'] and
            last_row['close'] < last_row['psar'] and 
            last_row['cci'] < -100
        )

