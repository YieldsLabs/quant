from ta.ATRIndicator import ATRIndicator
from tradetype import TradeType

class SimpleStopLossFinder:
    def __init__(self, stop_loss_pct=0.02):
        self.stop_loss_pct = stop_loss_pct

    def calculate_stop_loss_price(self, trade_type, entry_price):
        if trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price * (1.0 - self.stop_loss_pct)
        elif trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price * (1.0 + self.stop_loss_pct)
        
        return round(stop_loss_price, 2)
    
    def set_ohlcv(self, data):
        pass
    
    def __str__(self) -> str:
        return f'SimpleStopLossFinder(stop_loss_pct={self.stop_loss_pct})'
    
class LowHighStopLossFinder:
    def __init__(self, stop_loss_pct=0.002, lookback_period=10):
        self.simple_stop_loss = SimpleStopLossFinder(stop_loss_pct)
        self.lookback_period = lookback_period
        self.data = []

    def set_ohlcv(self, data):
        self.data = data

    def calculate_stop_loss_price(self, trade_type, entry_price=0):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = self.data.tail(self.lookback_period)
        entry_price = recent_data['low'].min() if trade_type.value == TradeType.LONG.value else recent_data['high'].max()

        return self.simple_stop_loss.calculate_stop_loss_price(trade_type, entry_price)
    
    def __str__(self) -> str:
        return f'LowHighStopLossFinder(stop_loss_pct={self.simple_stop_loss.stop_loss_pct}, lookback_period={self.lookback_period})'

class ATRStopLossFinder:
    def __init__(self, multiplier=1.5, atr_period=14):
        self.atr_indicator = ATRIndicator(atr_period)
        self.multiplier = multiplier
        self.data = []

    def set_ohlcv(self, data):
        self.data = data

    def calculate_stop_loss_price(self, entry_trade_type, entry_price):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')
    
        atr_value = self.atr_indicator.atr(self.data)
        atr_value = round(atr_value.iloc[-1], 2)

        if entry_trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price - (atr_value * self.multiplier)
        
        elif entry_trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price + (atr_value * self.multiplier)


        return round(stop_loss_price, 2)
    
    def __str__(self) -> str:
        return f'ATRStopLossFinder(multiplier={self.multiplier}, atr_period={self.atr_indicator.period})'


class TrailingStopLossFinder:
    def __init__(self, stop_loss_pct=0.002, lookback_period=10):
       self.low_high_stop_loss = LowHighStopLossFinder(stop_loss_pct=stop_loss_pct, lookback_period=lookback_period)
       self.initial_stop_loss = dict({
           TradeType.LONG.value: None,
           TradeType.SHORT.value: None,
       })
       self.data = []

    def set_ohlcv(self, data):
        self.data = data
        self.low_high_stop_loss.set_ohlcv(data)

    def calculate_stop_loss_price(self, trade_type, entry_price):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')

        if self.initial_stop_loss[trade_type.value] is None:
            self.initial_stop_loss.update({
                trade_type.value: self.low_high_stop_loss.calculate_stop_loss_price(trade_type, entry_price)
            })
        elif self._can_adjust_stop_loss(trade_type):
            self.initial_stop_loss.update({
                trade_type.value: self._adjust_stop_loss(trade_type, entry_price)
            })
        
        return  self.initial_stop_loss[trade_type.value]
    
    def _can_adjust_stop_loss(self, trade_type):
        return self.initial_stop_loss[trade_type.value] is not None
    
    def _adjust_stop_loss(self, trade_type, entry_price):
        current_row = self.data.iloc[-1]
        current_price = current_row['close']

        risk = abs(entry_price - self.initial_stop_loss[trade_type.value])
        reward = abs(current_price - entry_price)

        if trade_type.value == TradeType.LONG.value and reward >= risk:
            self.initial_stop_loss.update({
                trade_type.value: max(entry_price, self.calculate_stop_loss_price(trade_type, current_price))
            })
        elif trade_type.value == TradeType.SHORT.value and reward >= risk:
            self.initial_stop_loss.update({
                trade_type.value: min(entry_price, self.calculate_stop_loss_price(trade_type, current_price))
            })

        return self.initial_stop_loss[trade_type.value]
    
    def __str__(self) -> str:
        return f'TrailingStopLossFinder()'