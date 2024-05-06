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

        lookback = 6
        bb_factor = 2.0
        dist_mul = 0.382
        bbw_th = 0.02
        first_factor = 0.5
        second_factor = 1.0

        if len(ohlcvs) < lookback:
            return stop_loss_price, take_profit_price

        price = self._price(ohlcvs)
        high = min(ohlcvs[-lookback:], key=lambda x: abs(x.high - price)).high
        low = min(ohlcvs[-lookback:], key=lambda x: abs(x.low - price)).low

        upper_bb, lower_bb, middle_bb = self._bb(ohlcvs, lookback, bb_factor)
        bbw = (upper_bb - lower_bb) / middle_bb

        tr = self._true_ranges(ohlcvs)
        atr = self._ema(tr, lookback)
        atr_mul = first_factor * atr[-1]

        hist = [0]

        bull, bear = hist[-1] >= 0, hist[-1] < 0

        curr_dist = abs(entry_price - price)

        atr_first = first_factor * atr[-1]
        atr_second = second_factor * atr[-1]

        next_stop_loss = stop_loss_price

        # if entry_price != 0:
        #     profit_p = (abs(entry_price - price) / entry_price)
        # else:
        #     profit_p = 0

        if side == PositionSide.LONG:
            # tp_first = high + atr_first
            # tp_second = high + atr_second

            # tp = tp_first if price < tp_first else tp_second
            # tpp = tp_first if take_profit_price < tp_second and price > tp_first else tp

            # tp = min(take_profit_price, tp_first, tp_second)

            next_take_profit = max(
                take_profit_price,
                upper_bb[-1] + atr_mul if bbw[-1] > bbw_th else high + atr_mul,
            )

            dist = dist_mul * abs(entry_price - next_take_profit)

            if curr_dist > dist:
                next_stop_loss = max(
                    stop_loss_price, low - atr_mul, lower_bb[-1] - atr_mul
                )

            # profit = -1 * profit_p if price < entry_price else profit_p

            # print(f"Long - Bull: {bull}, Bear: {bear}, ATR: {atr_mul}, Profit: {round(profit * 100, 3)}, OHLCV: {ohlcvs[-1]}, ENTRY: {entry_price}, TP: {next_take_profit}, SL: {next_stop_loss}, BBD: {dist_bb}")

        elif side == PositionSide.SHORT:
            # tp_first = low - atr_first
            # tp_second = low - atr_second

            # tp = tp_first if price > tp_first else tp_second
            # tpp = tp_first if take_profit_price > tp_second and price < tp_first else tp
            # tp = max(take_profit_price, tp_first, tp_second)

            next_take_profit = min(
                take_profit_price,
                lower_bb[-1] - atr_mul if bbw[-1] > bbw_th else low - atr_mul,
            )

            dist = dist_mul * abs(entry_price - next_take_profit)

            if curr_dist > dist:
                next_stop_loss = min(
                    stop_loss_price, high + atr_mul, lower_bb[-1] + atr_mul
                )

            # profit = -1 * profit_p if price > entry_price else profit_p

            # print(f"SHORT - Bull: {bull}, Bear: {bear}, ATR: {atr_mul}, Profit: {round(profit * 100, 3)}, OHLCV: {ohlcvs[-1]}, ENTRY: {entry_price}, TP: {next_take_profit}, SL: {next_stop_loss}, BBD: {dist_bb}")

        return next_stop_loss, next_take_profit

    @staticmethod
    def _price(ohlcvs: List[OHLCV]) -> float:
        return (ohlcvs[-1].high + ohlcvs[-1].low + ohlcvs[-1].close) / 3.0

    @staticmethod
    def _bb(
        ohlcvs: List[OHLCV], period: int, factor: float
    ) -> Tuple[List[float], List[float], List[float]]:
        closes = np.array([ohlcv.close for ohlcv in ohlcvs])
        rolling_mean = np.convolve(closes, np.ones(period) / period, mode="valid")
        rolling_std = factor * np.std(
            [closes[i : i + period] for i in range(len(closes) - period + 1)], axis=1
        )

        return rolling_mean + rolling_std, rolling_mean - rolling_std, rolling_mean

    @staticmethod
    def _ema(values: List[float], period: int) -> List[float]:
        ema = [np.mean(values[:period])]

        alpha = 2 / (period + 1)

        for i in range(period, len(values)):
            ema.append((values[i] - ema[-1]) * alpha + ema[-1])

        return np.array(ema)

    @staticmethod
    def _true_ranges(ohlcvs: List[OHLCV]) -> List[float]:
        highs, lows, closes = (
            np.array([ohlcv.high for ohlcv in ohlcvs]),
            np.array([ohlcv.low for ohlcv in ohlcvs]),
            np.array([ohlcv.close for ohlcv in ohlcvs]),
        )

        prev_closes = np.roll(closes, 1)

        true_ranges = np.maximum(
            highs - lows, np.abs(highs - prev_closes), np.abs(lows - prev_closes)
        )

        return true_ranges
