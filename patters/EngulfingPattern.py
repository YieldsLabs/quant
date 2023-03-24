class EngulfingPattern:
    @staticmethod
    def bullish(data):
        bullish_engulfing_pattern = (data['close'].shift(1) < data['open'].shift(1)) & \
                                    (data['close'] > data['open']) & \
                                    (data['close'] > data['close'].shift(1)) & \
                                    (data['open'] < data['open'].shift(1))
        return bullish_engulfing_pattern

    @staticmethod
    def bearish(data):
        bearish_engulfing_pattern = (data['close'].shift(1) > data['open'].shift(1)) & \
                                    (data['close'] < data['open']) & \
                                    (data['close'] < data['close'].shift(1)) & \
                                    (data['open'] > data['open'].shift(1))
        return bearish_engulfing_pattern
