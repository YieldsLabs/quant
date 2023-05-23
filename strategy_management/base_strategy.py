from typing import List, Type, Union

import pandas as pd
from risk_management.stop_loss.finders.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.finders.abstract_take_profit_finder import AbstractTakeProfit
from .abstract_strategy import AbstractStrategy
from ta.alerts.abstract_alert import AbstractAlert
from ta.base.abstract_indicator import AbstractIndicator
from ta.patterns.abstract_pattern import AbstractPattern


class BaseStrategy(AbstractStrategy):
    def __init__(
        self,
        indicators: List[Union[AbstractIndicator, AbstractPattern]],
        stop_loss_finder: Type[AbstractStopLoss],
        risk_reward_ratio: float = 1.0
    ):
        super().__init__()
        self.indicators = indicators
        self.risk_reward_ratio = risk_reward_ratio
        self.stop_loss_finder = stop_loss_finder
        self.lookback: int = self._calculate_lookback()

    def _calculate_lookback(self):
        lookbacks = [item.lookback for item, _ in self.indicators if hasattr(item, 'lookback')] + \
                    [getattr(item, attr, 0) for item, _ in self.indicators for attr in dir(item) if attr.endswith('period')] + \
                    [getattr(obj, attr, 0) for obj in [self.stop_loss_finder] for attr in dir(obj) if attr.endswith('period')] + \
                    [getattr(self.stop_loss_finder, "lookback", 0)]

        return max(lookbacks, default=50)

    def _add_indicators_and_patterns(self, data: pd.DataFrame):
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

    def entry(self, ohlcv: pd.DataFrame):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)

        buy_entry = self._generate_buy_entry(data)
        sell_entry = self._generate_sell_entry(data)

        return buy_entry.iloc[-1], sell_entry.iloc[-1]

    def exit(self, ohlcv: pd.DataFrame):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)

        buy_exit = self._generate_buy_exit(data)
        sell_exit = self._generate_sell_exit(data)

        return buy_exit.iloc[-1], sell_exit.iloc[-1]

    def stop_loss(self, entry, ohlcv):
        stop_loss_long, stop_loss_short = self.stop_loss_finder.next(entry, ohlcv)

        return (stop_loss_long, stop_loss_short)

    def _generate_buy_entry(self, data: pd.DataFrame):
        raise NotImplementedError

    def _generate_sell_entry(self, data: pd.DataFrame):
        raise NotImplementedError

    def _generate_buy_exit(self, data: pd.DataFrame):
        return pd.Series(False)

    def _generate_sell_exit(self, data: pd.DataFrame):
        return pd.Series(False)

    def __str__(self):
        return f'{super().__str__()}{str(self.stop_loss_finder)}'
