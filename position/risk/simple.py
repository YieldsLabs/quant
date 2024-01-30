from typing import List

from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide


class PositionRiskSimpleStrategy(AbstractPositionRiskStrategy):
    def __init__(self):
        super().__init__()

    def next(
        self,
        _side: PositionSide,
        _entry_price: float,
        take_profit_price: float,
        stop_loss_price: float,
        _ohlcvs: List[OHLCV],
    ) -> float:
        return stop_loss_price, take_profit_price
