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
        
        return stop_loss_price
    
    def reset_stop_loss(self):
        pass

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

    def reset_stop_loss(self):
        pass

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

    def reset_stop_loss(self):
        pass

    def calculate_stop_loss_price(self, entry_trade_type, entry_price):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')
    
        atr_value = self.atr_indicator.atr(self.data)
        atr_value = atr_value.iloc[-1]

        if entry_trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price - (atr_value * self.multiplier)
        
        elif entry_trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price + (atr_value * self.multiplier)


        return stop_loss_price
    
    def __str__(self) -> str:
        return f'ATRStopLossFinder(multiplier={self.multiplier}, atr_period={self.atr_indicator.period})'

class TrailingStopLossFinder:
    def __init__(self, atr_multiplier=1.2, risk_reward_ratio=1.1, max_adjustments=20):
        self.low_high_stop_loss = ATRStopLossFinder(multiplier=atr_multiplier)
        self.risk_reward_ratio = risk_reward_ratio
        self.data = []
        self.reset_stop_loss()
        self.max_adjustments = max_adjustments

    def reset_stop_loss(self):
        self.current_stop_loss = { TradeType.LONG.value: None, TradeType.SHORT.value: None }
        self.adjustments = { TradeType.LONG.value: 0, TradeType.SHORT.value: 0 }

    def set_ohlcv(self, data):
        self.data = data
        self.low_high_stop_loss.set_ohlcv(data)

    def calculate_stop_loss_price(self, trade_type, entry_price):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')
        
        self.current_stop_loss[trade_type.value] = self.low_high_stop_loss.calculate_stop_loss_price(trade_type, entry_price)
        self.adjustments[trade_type.value] = 0

        while True:
            adjusted_stop_loss = self._adjust_stop_loss(trade_type, entry_price)
            if adjusted_stop_loss:
                print(f'Adjusted stop_loss={adjusted_stop_loss}')
                
                self.current_stop_loss[trade_type.value] = adjusted_stop_loss
                self.adjustments[trade_type.value] += 1
            else:
                break

            if self.adjustments[trade_type.value] >= self.max_adjustments:
                break

        return self.current_stop_loss[trade_type.value]

    def _adjust_stop_loss(self, trade_type, entry_price):
        current_row = self.data.iloc[-1]
        current_price = current_row['close']

        risk = abs(entry_price - self.current_stop_loss[trade_type.value])
        reward = abs(current_price - entry_price)
        
        risk_reward = risk / reward if reward != 0 else 0

        if trade_type.value == TradeType.LONG.value and risk_reward > self.risk_reward_ratio:
            new_stop_loss = max(entry_price, self.low_high_stop_loss.calculate_stop_loss_price(trade_type, entry_price))
        elif trade_type.value == TradeType.SHORT.value and risk_reward > self.risk_reward_ratio:
            new_stop_loss = max(entry_price, self.low_high_stop_loss.calculate_stop_loss_price(trade_type, entry_price))
        else:
            return
        
        if new_stop_loss >= self.current_stop_loss[trade_type.value]:
            return None
        
        return new_stop_loss

    def __str__(self) -> str:
        return f'TrailingStopLossFinder()'

