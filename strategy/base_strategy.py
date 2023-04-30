from typing import List, Type, Union
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from strategy.abstract_strategy import AbstractStrategy
from ta.alerts.abstract_alert import AbstractAlert
from ta.base.abstract_indicator import AbstractIndicator
from ta.patterns.abstract_pattern import AbstractPattern


class BaseStrategy(AbstractStrategy):
    def __init__(
        self,
        indicators: List[Union[AbstractIndicator, AbstractPattern]],
        take_profit_finder: Type[AbstractTakeProfit],
        stop_loss_finder: Type[AbstractStopLoss],
    ):
        super().__init__()
        self.indicators = indicators
        self.take_profit_finder = take_profit_finder
        self.stop_loss_finder = stop_loss_finder
        self.lookback: int = self._calculate_lookback()

    def _calculate_lookback(self):
        lookbacks = [item.lookback for item, _ in self.indicators if hasattr(item, 'lookback')] + \
                    [getattr(item, attr, 0) for item, _ in self.indicators for attr in dir(item) if attr.endswith('period')] + \
                    [getattr(obj, attr, 0) for obj in [self.stop_loss_finder, self.take_profit_finder] for attr in dir(obj) if attr.endswith('period')] + \
                    [getattr(self.stop_loss_finder, "lookback", 0), getattr(self.take_profit_finder, "lookback", 0)]

        return max(lookbacks, default=5) + 1

    def _add_indicators_and_patterns(self, data):
        for indicator, column in self.indicators:
            if isinstance(indicator, AbstractIndicator) or isinstance(indicator, AbstractAlert):
                indicator_output = indicator.call(data)
                if isinstance(indicator_output, tuple):
                    for res, col in zip(indicator_output, column):
                        data[col] = res
                else:
                    data[column] = indicator_output

            elif isinstance(indicator, AbstractPattern):
                bullish_column, bearish_column = column
                data[bullish_column], data[bearish_column] = indicator.bullish(data), indicator.bearish(data)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)

        buy_signal = self._generate_buy_signal(data)
        sell_signal = self._generate_sell_signal(data)

        return buy_signal.iloc[-1], sell_signal.iloc[-1]

    def exit(self, ohlcv):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)

        buy_exit = self._generate_buy_exit(data)
        sell_exit = self._generate_sell_exit(data)

        return buy_exit.iloc[-1], sell_exit.iloc[-1]

    def stop_loss_and_take_profit(self, entry, ohlcv):
        stop_loss_long, stop_loss_short = self.stop_loss_finder.next(entry, ohlcv)

        take_profit_long = self.take_profit_finder.next(entry, stop_loss_long)
        take_profit_short = self.take_profit_finder.next(entry, stop_loss_short)

        return ((stop_loss_long, take_profit_long), (stop_loss_short, take_profit_short))

    def _generate_buy_signal(self, data):
        raise NotImplementedError

    def _generate_sell_signal(self, data):
        raise NotImplementedError

    def _generate_buy_exit(self, data):
        raise NotImplementedError

    def _generate_sell_exit(self, data):
        raise NotImplementedError

    def __str__(self):
        return f'{super().__str__()}{str(self.take_profit_finder)}{str(self.stop_loss_finder)}'
