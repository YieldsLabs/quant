from typing import List, Tuple

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position_side import PositionSide


class PositionRiskFibonacciStrategy(AbstractPositionRiskStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")
        self.fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786]

    def next(
        self,
        side: PositionSide,
        entry_price: float,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcvs: List[Tuple[OHLCV]],
    ) -> float:
        ohlcvs = ohlcvs[:]
        lookback = 14

        if len(ohlcvs) < lookback:
            return stop_loss_price, take_profit_price

        atr = self._atr(ohlcvs, lookback)
        price = self._price(ohlcvs)

        risk_value = atr[-1] * self.config["risk_factor"]
        tp_threshold = atr[-1] * self.config["tp_factor"]

        high = min(ohlcvs[-lookback:], key=lambda x: abs(x.high - price)).high
        low = min(ohlcvs[-lookback:], key=lambda x: abs(x.low - price)).low

        next_stop_loss = stop_loss_price

        if side == PositionSide.LONG:
            next_take_profit = max(entry_price + risk_value, high + tp_threshold)

            for level in self.fibonacci_levels:
                retracement_price = entry_price + (high - entry_price) * level

                if retracement_price > stop_loss_price:
                    next_stop_loss = retracement_price
                    break

        elif side == PositionSide.SHORT:
            next_take_profit = min(entry_price - risk_value, low - tp_threshold)

            for level in self.fibonacci_levels:
                retracement_price = entry_price - (entry_price - low) * level

                if retracement_price < stop_loss_price:
                    next_stop_loss = retracement_price
                    break

        return next_stop_loss, next_take_profit

    @staticmethod
    def _atr(ohlcvs: List[OHLCV], period: int) -> float:
        highs, lows, closes = (
            np.array([ohlcv.high for ohlcv in ohlcvs]),
            np.array([ohlcv.low for ohlcv in ohlcvs]),
            np.array([ohlcv.close for ohlcv in ohlcvs]),
        )

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
        return (ohlcvs[-1].high + ohlcvs[-1].low + ohlcvs[-1].close) / 3.0
