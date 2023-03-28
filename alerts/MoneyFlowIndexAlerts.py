from ta.MoneyFlowIndexIndicator import MoneyFlowIndexIndicator


class MoneyFlowIndexAlerts:
    def __init__(self, period=14, overbought_level=80, oversold_level=20):
        self.mfi = MoneyFlowIndexIndicator(period)
        self.overbought_level = overbought_level
        self.oversold_level = oversold_level


    def alert(self, data):
        data = data.copy()
        data['mfi'] = self.mfi.mfi(data)

        return data['mfi'] < self.oversold_level, data['mfi'] > self.overbought_level