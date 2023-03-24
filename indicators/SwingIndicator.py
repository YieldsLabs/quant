class SwingIndicator:
    def _calculate_upside_momentum_gauge(self, row):
        if row['high'] > row['high_shifted'] and row['close'] > row['open']:
            return 2
        elif row['high'] > row['high_shifted'] and row['close'] < row['open']:
            return 1
        elif row['high'] < row['high_shifted'] and row['close'] > row['open']:
            return 1
        elif row['high'] < row['high_shifted'] and row['close'] < row['open']:
            return 0
        else:
            return 0

    def _calculate_downside_momentum_gauge(self, row):
        if row['low'] > row['low_shifted'] and row['close'] > row['open']:
            return 0
        elif row['low'] > row['low_shifted'] and row['close'] < row['open']:
            return 1
        elif row['low'] < row['low_shifted'] and row['close'] > row['open']:
            return 1
        elif row['low'] < row['low_shifted'] and row['close'] < row['open']:
            return 2
        else:
            return 0

    def swing(self, data):
        data = data.copy()

        data['high_shifted'] = data['high'].shift(1)
        data['low_shifted'] = data['low'].shift(1)

        data['upside_momentum_gauge'] = data.apply(
            self._calculate_upside_momentum_gauge, axis=1)
        data['downside_momentum_gauge'] = data.apply(
            self._calculate_downside_momentum_gauge, axis=1)

        data['raw_swing'] = data['upside_momentum_gauge'] - \
            data['downside_momentum_gauge']
        data['swing_indicator'] = data['raw_swing'].rolling(window=8).sum()

        return data['swing_indicator']
