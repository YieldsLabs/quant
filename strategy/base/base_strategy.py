from strategy.base.abstract_strategy import AbstractStrategy


class BaseStrategy(AbstractStrategy):
    def __init__(self, indicators, patterns=[]):
        super().__init__()
        self.indicators = indicators
        self.patterns = patterns
        self.lookback = self._calculate_lookback()

    def _calculate_lookback(self):
        lookbacks = [getattr(item, "lookback", 0) for items in [self.indicators, self.patterns] for item, _ in items]
        return max(lookbacks, default=5) + 1
    
    def _add_indicators_and_patterns(self, ohlcv):
        data = ohlcv.copy(deep=False)

        for indicator, column in self.indicators:
            indicator_output = indicator.call(data)
            if isinstance(indicator_output, tuple):
                for res, col in zip(indicator_output, column):
                    data[col] = res
            else:
                data[column] = indicator_output

        for pattern, (bullish_column, bearish_column) in self.patterns:
            data[bullish_column] = pattern.bullish(data)
            data[bearish_column] = pattern.bearish(data)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)

        buy_signal = self._generate_buy_signal(data)
        sell_signal = self._generate_sell_signal(data)

        return buy_signal, sell_signal

    def exit(self, ohlcv):
        return False, False

    def _generate_buy_signal(self, data):
        raise NotImplementedError

    def _generate_sell_signal(self, data):
        raise NotImplementedError
