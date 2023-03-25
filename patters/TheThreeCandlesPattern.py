class TheThreeCandlesPatterns:
    @staticmethod
    def three_white_soldiers(data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] > data['close'].shift(1)) & \
                    (data['close'].shift(1) > data['close'].shift(2)) & \
                    (data['close'].shift(2) > data['close'].shift(3)) & \
                    (body >= body.rolling(window=5).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition
    

    @staticmethod
    def three_black_crows(data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] < data['close'].shift(1)) & \
                    (data['close'].shift(1) < data['close'].shift(2)) & \
                    (data['close'].shift(2) < data['close'].shift(3)) & \
                    (body >= body.rolling(window=5).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition

