from typing import Callable, List, Tuple, Type, Union
import pandas as pd

from risk_management.stop_loss.finders.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.finders.abstract_take_profit_finder import AbstractTakeProfit
from ta.alerts.abstract_alert import AbstractAlert
from ta.base.abstract_indicator import AbstractIndicator
from ta.patterns.abstract_pattern import AbstractPattern

from .abstract_strategy import AbstractStrategy


class BaseStrategy(AbstractStrategy):
    MIN_LOOKBACK = 50

    def __init__(
        self,
        indicators: List[Tuple[Union[AbstractIndicator, AbstractPattern], Tuple[str]]],
        stop_loss_finder: Type[AbstractStopLoss],
        risk_reward_ratio: float = 1.0
    ):
        super().__init__()
        self._initialize_attributes(indicators, stop_loss_finder, risk_reward_ratio)
        self.lookback = self._calculate_lookback()

    def _initialize_attributes(self, indicators, stop_loss_finder, risk_reward_ratio):
        self.risk_reward_ratio = risk_reward_ratio
        self.stop_loss_finder = stop_loss_finder
        self.indicators, self.patterns = self._separate_indicators_and_patterns(indicators)

    def _separate_indicators_and_patterns(self, indicators):
        indicator_list = [ind for ind in indicators if isinstance(ind[0], (AbstractIndicator, AbstractAlert))]
        pattern_list = [ind for ind in indicators if isinstance(ind[0], AbstractPattern)]
        return indicator_list, pattern_list

    def _calculate_lookback(self):
        indicator_lookbacks = [indicator[0].lookback for indicator in self.indicators if hasattr(indicator[0], 'lookback')]
        indicator_periods = [getattr(indicator[0], attr, 0) for indicator in self.indicators for attr in dir(indicator[0]) if attr.endswith('period')]
        stop_loss_finder_periods = [getattr(self.stop_loss_finder, attr, 0) for attr in dir(self.stop_loss_finder) if attr.endswith('period')]
        stop_loss_finder_lookback = getattr(self.stop_loss_finder, "lookback", 0)

        all_lookbacks = indicator_lookbacks + indicator_periods + stop_loss_finder_periods + [stop_loss_finder_lookback] + [self.MIN_LOOKBACK]
        return max(all_lookbacks)

    def _add_indicators_and_patterns(self, data: pd.DataFrame):
        for indicator, column in self.indicators:
            indicator_output = indicator.call(data)
            if isinstance(indicator_output, tuple):
                for res, col in zip(indicator_output, column):
                    data[col] = res
            else:
                data[column] = indicator_output

        for pattern, column in self.patterns:
            bullish_column, bearish_column = column
            data[bullish_column] = pattern.bullish(data)
            data[bearish_column] = pattern.bearish(data)

        return data

    def _process_data(self, ohlcv: pd.DataFrame, generate_func: Callable):
        if len(ohlcv) < self.lookback:
            return False, False

        data = self._add_indicators_and_patterns(ohlcv)
        buy_data = generate_func(data)
        sell_data = generate_func(data)

        return buy_data.iloc[-1], sell_data.iloc[-1]

    def entry(self, ohlcv: pd.DataFrame):
        return self._process_data(ohlcv, self._generate_buy_entry), self._process_data(ohlcv, self._generate_sell_entry)

    def exit(self, ohlcv: pd.DataFrame):
        return self._process_data(ohlcv, self._generate_buy_exit), self._process_data(ohlcv, self._generate_sell_exit)

    def stop_loss(self, entry, ohlcv):
        stop_loss_long, stop_loss_short = self.stop_loss_finder.next(entry, ohlcv)
        return stop_loss_long, stop_loss_short

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
