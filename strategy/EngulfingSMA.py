from buy_sell.MoneyFlowIndexAlerts import MoneyFlowIndexAlerts
from strategy.AbstractStrategy import AbstractStrategy
from patters.EngulfingPattern import EngulfingPattern
from ta.MovingAverageIndicator import MovingAverageIndicator


class EngulfingSMA(AbstractStrategy):
    def __init__(self, slow_sma_period=100, upper_barrier=80, lower_barrier=20, pullback_window=3, tolerance=0.02):
        super().__init__()
        self.slow_sma = MovingAverageIndicator(slow_sma_period)
        self.mfi = MoneyFlowIndexAlerts(overbought_level=upper_barrier, oversold_level=lower_barrier)
        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier
        self.pullback_window = pullback_window
        self.tolerance = tolerance

    def add_indicators(self, data):
        data = data.copy()
        data['sma_slow'] = self.slow_sma.smma(data['close'])

        data['bullish_engulfing'] = EngulfingPattern.bullish(data)
        data['bearish_engulfing'] = EngulfingPattern.bearish(data)

        data['mfi_buy'], data['mfi_sell'] = self.mfi.alert(data)

        return data
    
    def check_confirmation_candle(self, current_row, previous_row):
        buy_confirmation = (
            previous_row['close'] > current_row['sma_slow']
            and abs(previous_row['close'] - current_row['sma_slow']) / current_row['sma_slow'] <= self.tolerance
        )
        sell_confirmation = (
            previous_row['close'] < current_row['sma_slow']
            and abs(previous_row['close'] - current_row['sma_slow']) / current_row['sma_slow'] <= self.tolerance
        )
        
        return buy_confirmation, sell_confirmation

    def check_pullback(self, data):
        pullback_data = data[-self.pullback_window:]
        sma_pullback = pullback_data['sma_slow'].min() < pullback_data['close'].min()
        return sma_pullback

    def entry(self, data):
        if len(data) < max(3, self.pullback_window):
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        buy_confirmation, sell_confirmation = self.check_confirmation_candle(current_row, previous_row)
        
        # pullback = self.check_pullback(data)

        buy_signal = (
            buy_confirmation and
            current_row['bullish_engulfing'] and
            current_row['mfi_buy']
            # pullback
        )

        sell_signal = (
            sell_confirmation and
            current_row['bearish_engulfing'] and
            current_row['mfi_sell']
        )

        return buy_signal, sell_signal
    
    def __str__(self) -> str:
        return f'EngulfingSMA(slow_sma_period={self.slow_sma.window})'
