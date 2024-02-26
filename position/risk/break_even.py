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
        ohlcvs: List[Tuple[OHLCV, bool]],
    ) -> float:
        lookback_window = 3
        closed_ohlcv = [ohlcv for ohlcv, closed in ohlcvs if closed]

        if len(closed_ohlcv) < lookback_window:
            return stop_loss_price, take_profit_price

        next_stop_loss = stop_loss_price
        next_take_profit = take_profit_price

        wicks = [ohlcv for ohlcv, _ in ohlcvs]
        recent_low = min(ohlcv.low for ohlcv in closed_ohlcv)
        recent_high = max(ohlcv.high for ohlcv in closed_ohlcv)

        atr = self._atr(closed_ohlcv, lookback_window)
        atr_val = atr[-1]

        risk_value = atr_val * self.config["risk_factor"]
        tp_threshold = atr_val * self.config["tp_factor"]

        if side == PositionSide.LONG:
            sl = max(next_stop_loss, entry_price + risk_value, recent_low - risk_value)
            dist = (
                abs(entry_price - next_take_profit - risk_value)
                * self.config["sl_factor"]
            )

            if (
                closed_ohlcv[-1].high >= entry_price + dist
                and sl < closed_ohlcv[-1].low
            ):
                next_stop_loss = sl

            if wicks[-1].high >= next_take_profit - tp_threshold:
                current_price = self._price(closed_ohlcv)

                next_take_profit = max(
                    next_take_profit,
                    current_price
                    + (current_price - stop_loss_price)
                    * self.config["risk_reward_ratio"],
                )

                next_stop_loss = sl

        elif side == PositionSide.SHORT:
            sl = min(next_stop_loss, entry_price - risk_value, recent_high + risk_value)
            dist = (
                abs(entry_price - next_take_profit + risk_value)
                * self.config["sl_factor"]
            )

            if (
                closed_ohlcv[-1].low <= entry_price - dist
                and sl > closed_ohlcv[-1].high
            ):
                next_stop_loss = sl

            if wicks[-1].low <= next_take_profit + tp_threshold:
                current_price = self._price(closed_ohlcv)
                next_take_profit = min(
                    next_take_profit,
                    current_price
                    - (next_stop_loss - current_price)
                    * self.config["risk_reward_ratio"],
                )
                next_stop_loss = sl

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
