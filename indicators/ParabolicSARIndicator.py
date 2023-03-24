class ParabolicSARIndicator:
    def __init__(self, start=0.02, increment=0.02, maximum=0.2):
        self.start = start
        self.increment = increment
        self.maximum = maximum

    def parabolic_sar(self, ohlcv):
        data = ohlcv.copy()
        data['psar'] = data['close'].values

        initial = self.start
        step = self.increment
        max_step = self.maximum

        trend = 1
        extreme_point = data['high'][0]
        accel_factor = initial
        data.at[0, 'psar'] = data['low'][0]

        for i in range(1, len(data)):
            temp_psar = data.at[i - 1, 'psar'] + accel_factor * (extreme_point - data.at[i - 1, 'psar'])
            if trend == 1:
                data.at[i, 'psar'] = min(temp_psar, data.at[i - 1, 'low'])
                if data.at[i, 'high'] > extreme_point:
                    extreme_point = data.at[i, 'high']
                    accel_factor = min(accel_factor + step, max_step)
                if data.at[i, 'psar'] > data.at[i, 'low']:
                    accel_factor = initial
                    trend = -1
                    data.at[i, 'psar'] = extreme_point
                    extreme_point = data.at[i, 'low']
            else:
                data.at[i, 'psar'] = max(temp_psar, data.at[i - 1, 'high'])
                if data.at[i, 'low'] < extreme_point:
                    extreme_point = data.at[i, 'low']
                    accel_factor = min(accel_factor + step, max_step)
                if data.at[i, 'psar'] < data.at[i, 'high']:
                    accel_factor = initial
                    trend = 1
                    data.at[i, 'psar'] = extreme_point
                    extreme_point = data.at[i, 'high']

        return data['psar']