from collections import deque
from typing import List, Tuple

import numpy as np
from sklearn.linear_model import SGDRegressor

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position_side import PositionSide


class PositionRiskVolatilityStrategy(AbstractPositionRiskStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")
        self.tp_model = SGDRegressor(max_iter=50, tol=1e-3)
        self.sl_model = SGDRegressor(max_iter=50, tol=1e-3)

        self.x_tp_buff = deque(maxlen=55)
        self.y_tp_buff = deque(maxlen=55)

        self.x_sl_buff = deque(maxlen=55)
        self.y_sl_buff = deque(maxlen=55)
        self.lookback = 6

    def next(
        self,
        side: PositionSide,
        entry_price: float,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcvs: List[Tuple[OHLCV]],
    ) -> float:
        ohlcvs = ohlcvs[:]

        if len(ohlcvs) < self.lookback:
            return stop_loss_price, take_profit_price

        atr = self._atr(ohlcvs, self.lookback)
        price = self._hlc(ohlcvs)
        mean = np.mean(price)
        std = np.std(price)

        curr_price, curr_atr = price[-1], atr[-1]

        features = self._features(ohlcvs, atr)

        self.update_tp_model(features, np.array([take_profit_price]))
        self.update_sl_model(features, np.array([stop_loss_price]))

        risk_value = curr_atr * self.config["risk_factor"]
        sl_threshold = curr_atr * self.config["sl_factor"]
        tp_threshold = curr_atr * self.config["tp_factor"]

        tsl = abs(entry_price - take_profit_price) * self.config["trl_factor"]
        curr_dist = abs(entry_price - curr_price)

        high = min(ohlcvs[-self.lookback :], key=lambda x: abs(x.high - tsl)).high
        low = min(ohlcvs[-self.lookback :], key=lambda x: abs(x.low - tsl)).low

        next_stop_loss, next_take_profit = stop_loss_price, take_profit_price

        upper_bound, lower_bound = mean + 2 * std, mean - 2 * std

        predict_tp = self.predict_take_profit(
            upper_bound, lower_bound, take_profit_price, side, tp_threshold
        )

        predict_sl = self.predict_stop_loss(
            upper_bound, lower_bound, stop_loss_price, side, sl_threshold
        )

        print(
            f"PREDICT: ENTRY: {entry_price}, TP: {predict_tp}, SL: {predict_sl}, SIDE: {side}, PRICE: {curr_price},  TSL: {tsl}"
        )

        if side == PositionSide.LONG:
            if predict_tp > curr_price:
                next_take_profit = max(entry_price + risk_value, predict_tp)

            if predict_sl < curr_price:
                next_stop_loss = max(
                    stop_loss_price,
                    low - tp_threshold,
                    predict_sl,
                )

        elif side == PositionSide.SHORT:
            if predict_tp < curr_price:
                next_take_profit = min(entry_price - risk_value, predict_tp)

            if predict_sl > curr_price:
                next_stop_loss = min(
                    stop_loss_price,
                    high + sl_threshold,
                    predict_sl,
                )

        return next_stop_loss, next_take_profit

    def predict_take_profit(
        self,
        upper_bound: float,
        lower_bound: float,
        take_profit_price: float,
        side: PositionSide,
        buff: float,
    ) -> float:
        if len(self.x_tp_buff) < self.lookback:
            return take_profit_price

        latest_X = self.x_tp_buff[-1]
        prediction = self.tp_model.predict(latest_X)

        tpp = abs(prediction[0])

        if tpp > upper_bound or tpp < lower_bound:
            return take_profit_price

        if side == PositionSide.LONG:
            return tpp + buff
        else:
            return tpp - buff

    def predict_stop_loss(
        self,
        upper_bound: float,
        lower_bound: float,
        stop_loss_price: float,
        side: PositionSide,
        buff: float,
    ) -> float:
        if len(self.x_sl_buff) < self.lookback:
            return stop_loss_price

        latest_X = self.x_sl_buff[-1]
        prediction = self.sl_model.predict(latest_X)

        slp = abs(prediction[0])

        if slp > upper_bound or slp < lower_bound:
            return stop_loss_price

        if side == PositionSide.LONG:
            return slp - buff
        else:
            return slp + buff

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
    def _hlc2(ohlcvs: List[OHLCV]) -> List[float]:
        return [(ohlcv.high + ohlcv.low + 2 * ohlcv.close) / 4.0 for ohlcv in ohlcvs]

    @staticmethod
    def _hlc(ohlcvs: List[OHLCV]) -> List[float]:
        return [(ohlcv.high + ohlcv.low + ohlcv.close) / 3.0 for ohlcv in ohlcvs]

    @staticmethod
    def _pp(ohlcvs: List[OHLCV]):
        previous_close = ohlcvs[-2].close
        previous_high = ohlcvs[-2].high
        previous_low = ohlcvs[-2].low

        pivot_point = (previous_high + previous_low + previous_close) / 3

        support1 = (2 * pivot_point) - previous_high
        resistance1 = (2 * pivot_point) - previous_low

        support2 = pivot_point - (previous_high - previous_low)
        resistance2 = pivot_point + (previous_high - previous_low)

        return support1, resistance1, support2, resistance2

    def _features(self, ohlcvs: List[Tuple[OHLCV]], atr: List[float]):
        support1, resistance1, support2, resistance2 = self._pp(ohlcvs)
        closes = [ohlcv.close for ohlcv in ohlcvs]
        mean_vol = np.mean([ohlcv.volume for ohlcv in ohlcvs])

        mean = np.mean(closes)
        std = np.std(closes)

        features = np.array(
            [
                self._hlc(ohlcvs)[-1],
                self._hlc2(ohlcvs)[-1],
                3 * atr[-1],
                mean - 2 * std,
                mean + 2 * std,
                support1,
                resistance1,
                support2,
                resistance2,
                ohlcvs[-1].volume / mean_vol,
            ]
        )

        features = (features - np.mean(features)) / np.std(features)

        return features.reshape(1, -1)

    def update_tp_model(self, X, y):
        self.x_tp_buff.append(X)
        self.y_tp_buff.append(y)

        if len(self.x_tp_buff) > self.lookback:
            X_train = np.vstack(self.x_tp_buff)
            y_train = np.vstack(self.y_tp_buff).ravel()

            self.tp_model.partial_fit(X_train, y_train)

    def update_sl_model(self, X, y):
        self.x_sl_buff.append(X)
        self.y_sl_buff.append(y)

        if len(self.x_sl_buff) > self.lookback:
            X_train = np.vstack(self.x_sl_buff)
            y_train = np.vstack(self.y_sl_buff).ravel()

            self.sl_model.partial_fit(X_train, y_train)
