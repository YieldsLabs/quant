from typing import List, Tuple

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position_side import PositionSide


class PositionRiskVolatilityStrategy(AbstractPositionRiskStrategy):
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
        ohlcvs = ohlcvs[:]
        lookback = 3

        if len(ohlcvs) < lookback + 3:
            return stop_loss_price, take_profit_price

        atr = self._atr(ohlcvs, lookback)
        price = self._price(ohlcvs)

        distance = atr[-1] * self.config["trl_factor"]
        tp_threshold = atr[-1] * self.config["tp_factor"]
        sl_threshold = atr[-1] * self.config["sl_factor"]

        tsl = abs(entry_price - price) * distance

        next_stop_loss = stop_loss_price

        if side == PositionSide.LONG:
            next_take_profit = max(entry_price + tp_threshold, take_profit_price - tsl)

            if price > tsl and price > entry_price:
                next_stop_loss = max(entry_price - sl_threshold, stop_loss_price + tsl)

        elif side == PositionSide.SHORT:
            next_take_profit = max(entry_price - tp_threshold, take_profit_price + tsl)

            if price > tsl and price < entry_price:
                next_stop_loss = min(entry_price + sl_threshold, stop_loss_price - tsl)

        return next_stop_loss, next_take_profit

    @staticmethod
    def _atr(ohlcvs: List[OHLCV], period: int) -> List[float]:
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

        return list(atr)

    @staticmethod
    def _price(ohlcvs: List[OHLCV]) -> float:
        return (ohlcvs[-1].high + ohlcvs[-1].low + 2 * ohlcvs[-1].close) / 4.0
