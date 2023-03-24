from strategy.AbstractStrategy import AbstractStrategy
from indicators.SwingIndicator import SwingIndicator


class SwingIndicatorStrategy(AbstractStrategy):
    def __init__(self):
        super().__init__()
        self.swing_indicator = SwingIndicator()

    def add_indicators(self, data):
        data = data.copy()
        data['swing_indicator'] = self.swing_indicator.swing(data)
        return data

    def entry(self, data):
        if len(data) < 5:
            return False, False

        data = self.add_indicators(data)

        last_row = data.iloc[-1]
        previous_rows = data.iloc[-5:-1]

        buy_signal = (
            last_row['swing_indicator'] <= -10
            and all(previous_rows['swing_indicator'] > -10)
        )

        sell_signal = (
            last_row['swing_indicator'] >= 10
            and all(previous_rows['swing_indicator'] < 10)
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'SwingIndicatorStrategy'
