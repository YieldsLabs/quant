from indicators.HigherHighLowerLowIndicator import HigherHighLowerLowIndicator
from buy_sell.UTBotAlerts import UTBotAlerts
from strategy.AbstractStrategy import AbstractStrategy
from ta.BBIndicator import BBIndicator

class UTBotAlertsBBStrategy(AbstractStrategy):
    def __init__(self, atr_period=10, sensitivity=1, ema_period=1, bb_period=20, bb_std_dev=2, hh_ll_left_bars=5, hh_ll_right_bars=5):
        super().__init__()
        self.ut_bot_alerts = UTBotAlerts(atr_period=atr_period, sensitivity=sensitivity,
                                                  ema_period=ema_period)
        self.bb = BBIndicator(sma_period=bb_period, multiplier=bb_std_dev)
        # self.hh_ll_indicator = HigherHighLowerLowIndicator(hh_ll_left_bars, hh_ll_right_bars)
        self.position = 0  # 1 for long, -1 for short, 0 for no position

    def add_indicators(self, data):
        data = data.copy()
        buy_signal, sell_signal = self.ut_bot_alerts.alert(data)
        data['buy_signal'] = buy_signal
        data['sell_signal'] = sell_signal
        data['upper_band'], data['lower_band'] = self.bb.bb(data)
        # data['hh'], data['ll'] = self.hh_ll_indicator.hh_ll(data)
        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]

        buy_signal = False
        sell_signal = False

        if current_row['buy_signal'] and self.position != 1 and current_row['close'] <= current_row['upper_band']:
            buy_signal = True
            self.position = 1
        elif current_row['sell_signal'] and self.position != -1 and current_row['close'] >= current_row['lower_band']:
            sell_signal = True
            self.position = -1

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'UTBotAlertsBBStrategy'
