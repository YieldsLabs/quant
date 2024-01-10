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
        ohlcv: OHLCV,
    ) -> float:
        current_price = self._weighted_typical_price(ohlcv)
        rrr = self.config["risk_reward_ratio"]
        factor = self.config["tsl_distance"]


        if side == PositionSide.LONG and current_price >= take_profit_price:
            print('May be next long ?')
            next_stop_loss = max(stop_loss_price, current_price * factor)
            next_take_profit = max(
                take_profit_price,
                rrr * (current_price - next_stop_loss) + current_price,
            )

            return next_stop_loss, next_take_profit

        if side == PositionSide.SHORT and current_price <= take_profit_price:
            print('May be next short ?')
            next_stop_loss = min(stop_loss_price, current_price * factor)
            next_take_profit = min(
                take_profit_price,
                rrr * (current_price - next_stop_loss) + current_price,
            )

            return next_stop_loss, next_take_profit

        return stop_loss_price, take_profit_price

    @staticmethod
    def _weighted_typical_price(ohlcv: OHLCV) -> float:
        return (ohlcv.high + ohlcv.low + (ohlcv.close * 2.0)) / 4.0
