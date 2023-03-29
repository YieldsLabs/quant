
class RSIIndicator:
    def __init__(self, period=14):
        self.period = period

    def rsi(self, data, column='close'):
        delta = data[column].diff()
        gain, loss = delta.copy(), delta.copy()
        gain[gain < 0] = 0
        loss[loss > 0] = 0
        loss = loss.abs()

        avg_gain = gain.rolling(window=self.period).mean()
        avg_loss = loss.rolling(window=self.period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi
