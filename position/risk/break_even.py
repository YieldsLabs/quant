from typing import List, Tuple

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.side import PositionSide


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
        lookback = 14
        factor = 2.0

        if len(ohlcvs) < lookback:
            return stop_loss_price, take_profit_price

        atr = self._atr(ohlcvs, lookback)
        price = self._price(ohlcvs)

        risk_value = atr[-1] * self.config["risk_factor"]
        tp_threshold = atr[-1] * self.config["tp_factor"]
        sl_threshold = atr[-1] * self.config["sl_factor"]

        dist = abs(entry_price - take_profit_price) * self.config["trl_factor"]
        curr_dist = abs(entry_price - price)

        high = min(ohlcvs[-lookback:], key=lambda x: abs(x.high - price)).high
        low = min(ohlcvs[-lookback:], key=lambda x: abs(x.low - price)).low

        upper_bb, lower_bb, middle_bb = self._bb(ohlcvs, lookback, factor)
        bbw = (upper_bb - lower_bb) / middle_bb
        
        squeeze = bbw <= np.min(bbw[-lookback:])

        next_stop_loss = stop_loss_price

        if side == PositionSide.LONG:
            if squeeze[-1]:
                next_take_profit = max(entry_price + risk_value, upper_bb[-1])
            else:
               next_take_profit = max(entry_price + risk_value, high + tp_threshold) 

            if curr_dist > dist and price > entry_price:
                next_stop_loss = max(entry_price - risk_value, low - sl_threshold)

        elif side == PositionSide.SHORT:
            if squeeze[-1]:
                next_take_profit = min(entry_price - risk_value, lower_bb[-1])
            else:
               next_take_profit = min(entry_price - risk_value, low - tp_threshold) 

            if curr_dist > dist and price < entry_price:
                next_stop_loss = min(entry_price + risk_value, high + sl_threshold)

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

        return atr

    @staticmethod
    def _price(ohlcvs: List[OHLCV]) -> float:
        return (ohlcvs[-1].high + ohlcvs[-1].low + ohlcvs[-1].close) / 3.0

    @staticmethod
    def _bb(ohlcvs: List[OHLCV], period: int, factor: float) -> Tuple[List[float], List[float], List[float]]:
        closes = np.array([ohlcv.close for ohlcv in ohlcvs])
        rolling_mean = np.convolve(closes, np.ones(period) / period, mode='valid')
        rolling_std = factor * np.std([closes[i:i+period] for i in range(len(closes) - period + 1)], axis=1)
    
        return rolling_mean + rolling_std, rolling_mean - rolling_std, rolling_mean