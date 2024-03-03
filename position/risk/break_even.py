from typing import List, Tuple

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position_side import PositionSide


class PositionRiskBreakEvenStrategy(AbstractPositionRiskStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")

    def next(
        self,
        side: PositionSide,
        entry_price: float,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcvs: List[Tuple[OHLCV]],
    ) -> float:
        next_stop_loss = stop_loss_price
        next_take_profit = take_profit_price

        if len(ohlcvs) < 2:
            return next_stop_loss, next_take_profit

        lookback_window = 3

        recent_high = max([ohlcv.high for ohlcv in ohlcvs[-lookback_window:]])
        recent_low = min([ohlcv.low for ohlcv in ohlcvs[-lookback_window:]])

        atr = self._atr(ohlcvs, lookback_window)
        atr_val = atr[-1]
        curr_price = self._price(ohlcvs)

        risk_value = atr_val * self.config["risk_factor"]
        tp_threshold = atr_val * self.config["tp_factor"]
        sl_threshold = atr_val * self.config["sl_factor"]

        if side == PositionSide.LONG:
            if curr_price >= entry_price + sl_threshold:
                next_stop_loss = max(
                    next_stop_loss, entry_price - risk_value, recent_low - risk_value
                )

            if recent_high >= entry_price + tp_threshold:
                next_take_profit = max(
                    entry_price + risk_value, recent_high + risk_value
                )

        elif side == PositionSide.SHORT:
            if curr_price <= entry_price - sl_threshold:
                next_stop_loss = min(
                    next_stop_loss, entry_price + risk_value, recent_high + risk_value
                )

            if recent_low <= entry_price - tp_threshold:
                next_take_profit = min(
                    entry_price - risk_value, recent_low - risk_value
                )

        return next_stop_loss, next_take_profit

    @staticmethod
    def _atr(ohlcvs: List[OHLCV], period: int) -> float:
        highs = np.array([ohlcv.high for ohlcv in ohlcvs])
        lows = np.array([ohlcv.low for ohlcv in ohlcvs])
        closes = np.array([ohlcv.close for ohlcv in ohlcvs])

        prev_closes = np.roll(closes, 1)

        true_ranges = np.maximum(
            highs - lows, np.abs(highs - prev_closes), np.abs(lows - prev_closes)
        )

        atr = np.zeros_like(true_ranges, dtype=float)
        atr[period - 1] = np.mean(true_ranges[:period])

        for i in range(period, len(true_ranges)):
            atr[i] = np.divide((atr[i - 1] * (period - 1) + true_ranges[i]), period)

        return atr

    @staticmethod
    def _price(ohlcvs: List[OHLCV]) -> float:
        return (ohlcvs[-1].high + ohlcvs[-1].low + 2 * ohlcvs[-1].close) / 4.0
