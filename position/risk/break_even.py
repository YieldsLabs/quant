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
        ohlcvs = ohlcvs[:]

        if len(ohlcvs) < 2:
            return stop_loss_price, take_profit_price

        lookback = 14
        factor = 2.0

        atr = self._atr(ohlcvs, lookback)
        price = self._price(ohlcvs)

        risk_value = atr[-1] * self.config["risk_factor"]
        tp_threshold = atr[-1] * self.config["tp_factor"]
        sl_threshold = atr[-1] * self.config["sl_factor"]

        dist = abs(entry_price - take_profit_price) * self.config["be_factor"]
        curr_dist = abs(entry_price - price)

        high = min(ohlcvs[-lookback:], key=lambda x: abs(x.high - price)).high
        low = min(ohlcvs[-lookback:], key=lambda x: abs(x.low - price)).low

        upper_band, lower_band = self._bb(ohlcvs, lookback, factor)
        next_stop_loss = stop_loss_price

        if side == PositionSide.LONG:
            next_stop_loss = max(stop_loss_price, low - sl_threshold)
            next_take_profit = max(
                entry_price + risk_value, high + tp_threshold, upper_band
            )

            if curr_dist > dist and ohlcvs[-1].low > entry_price:
                next_stop_loss = max(
                    stop_loss_price, entry_price - risk_value, low - sl_threshold
                )

        elif side == PositionSide.SHORT:
            next_stop_loss = min(stop_loss_price, high + sl_threshold)
            next_take_profit = min(
                entry_price - risk_value, low - tp_threshold, lower_band
            )

            if curr_dist > dist and ohlcvs[-1].high < entry_price:
                next_stop_loss = min(
                    stop_loss_price, entry_price + risk_value, high + sl_threshold
                )

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
    def _bb(ohlcvs: List[OHLCV], period: int, factor: float) -> float:
        prices = np.array([ohlcv.close for ohlcv in ohlcvs[-period:]])
        moving_avg = np.mean(prices)
        std_dev = np.std(prices)

        upper_band = moving_avg + factor * std_dev
        lower_band = moving_avg - factor * std_dev

        return upper_band, lower_band

    @staticmethod
    def _price(ohlcvs: List[OHLCV]) -> float:
        return (ohlcvs[-1].high + ohlcvs[-1].low + ohlcvs[-1].close) / 3.0
