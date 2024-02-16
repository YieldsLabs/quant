from typing import List

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
        ohlcvs: List[OHLCV],
    ) -> float:
        lookback_window = 3
        recent_low = min(ohlcv.low for ohlcv in ohlcvs[-lookback_window:])
        recent_high = max(ohlcv.high for ohlcv in ohlcvs[-lookback_window:])

        next_stop_loss = stop_loss_price
        next_take_profit = take_profit_price
        ohlcv = ohlcvs[-1]

        current_price = self._price(ohlcv)
        atr = self.atr(ohlcvs, lookback_window)
        atr_val = atr[-1]

        risk_value = atr_val * self.config["risk_factor"]
        tp_threshold = atr_val * self.config["tp_factor"]
        dist = abs(entry_price - next_take_profit) * self.config["sl_factor"]

        if side == PositionSide.LONG:
            if ohlcv.high >= entry_price + dist and next_stop_loss <= entry_price:
                next_stop_loss = max(next_stop_loss, entry_price + risk_value)

            if ohlcv.high >= next_take_profit - tp_threshold:
                next_take_profit = max(
                    next_take_profit,
                    current_price
                    + tp_threshold
                    + (current_price + tp_threshold - next_stop_loss)
                    * self.config["risk_reward_ratio"],
                )
                next_stop_loss = max(next_stop_loss, recent_low - risk_value)

        elif side == PositionSide.SHORT:
            if ohlcv.low <= entry_price - dist and next_stop_loss >= entry_price:
                next_stop_loss = min(next_stop_loss, entry_price - risk_value)

            if ohlcv.low <= take_profit_price + tp_threshold:
                next_take_profit = min(
                    next_take_profit,
                    current_price
                    - tp_threshold
                    - (next_stop_loss - current_price - tp_threshold)
                    * self.config["risk_reward_ratio"],
                )
                next_stop_loss = min(next_stop_loss, recent_high + risk_value)

        return next_stop_loss, next_take_profit

    @staticmethod
    def atr(ohlcvs: List[OHLCV], period: int) -> float:
        highs = np.array([ohlc.high for ohlc in ohlcvs])
        lows = np.array([ohlc.low for ohlc in ohlcvs])
        closes = np.array([ohlc.close for ohlc in ohlcvs])

        true_ranges = np.maximum(
            highs - lows, np.abs(highs - closes), np.abs(lows - closes)
        )
        tr_rolling = np.convolve(true_ranges, np.ones(period), "valid") / period

        return tr_rolling

    @staticmethod
    def _price(ohlcv: OHLCV) -> float:
        return (ohlcv.high + ohlcv.low + 2 * ohlcv.close) / 4.0
