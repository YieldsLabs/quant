from typing import List

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide


class PositionRiskBreakEvenStrategy(AbstractPositionRiskStrategy):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("position")

    def next(
        self,
        side: PositionSide,
        take_profit_price: float,
        stop_loss_price: float,
        ohlcvs: List[OHLCV],
    ) -> float:
        lookback_window = 8
        recent_low = min(ohlcv.low for ohlcv in ohlcvs[-lookback_window:])
        recent_high = max(ohlcv.high for ohlcv in ohlcvs[-lookback_window:])

        next_stop_loss = stop_loss_price
        next_take_profit = take_profit_price
        ohlcv = ohlcvs[-1]

        current_price = self._weighted_typical_price(ohlcv)
        atr = self.atr(ohlcvs, 14)
        risk_value = atr * self.config["risk_atr_multi"]
        tp_threshold = atr * self.config["tp_threshold"]

        if side == PositionSide.LONG:
            next_stop_loss = max(stop_loss_price, recent_low - risk_value)

            if ohlcv.high >= take_profit_price - tp_threshold:
                next_take_profit = max(
                    take_profit_price,
                    self.config["risk_reward_ratio"] * (current_price - next_stop_loss)
                    + current_price,
                )

        elif side == PositionSide.SHORT:
            next_stop_loss = min(stop_loss_price, recent_high + risk_value)

            if ohlcv.low <= take_profit_price + tp_threshold:
                next_take_profit = min(
                    take_profit_price,
                    self.config["risk_reward_ratio"] * (current_price - next_stop_loss)
                    + current_price,
                )

        return next_stop_loss, next_take_profit

    @staticmethod
    def atr(ohlcvs: List[OHLCV], period: int) -> float:
        def true_range(ohlc: OHLCV) -> float:
            return np.max(
                [
                    ohlc.high - ohlc.low,
                    np.abs(ohlc.high - ohlc.close),
                    np.abs(ohlc.low - ohlc.close),
                ]
            )

        tr_list = np.array([true_range(ohlc) for ohlc in ohlcvs[-period:]])

        return np.sum(tr_list) / period

    @staticmethod
    def _weighted_typical_price(ohlcv: OHLCV) -> float:
        return (ohlcv.high + ohlcv.low + (ohlcv.close * 2.0)) / 4.0
