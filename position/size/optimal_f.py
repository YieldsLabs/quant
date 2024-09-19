from core.interfaces.abstract_order_size_strategy import AbstractOrderSizeStrategy
from core.models.entity.signal import Signal
from core.models.size import PositionSizeType
from core.queries.portfolio import GetPositionRisk


class PositionOptimalFSizeStrategy(AbstractOrderSizeStrategy):
    def __init__(self):
        super().__init__()

    async def calculate(
        self,
        signal: Signal,
    ) -> float:
        risk_amount = await self.query(
            GetPositionRisk(signal, PositionSizeType.Optimalf)
        )

        if signal.stop_loss is not None and signal.entry is not None:
            price_difference = abs(signal.entry - signal.stop_loss)
        else:
            raise ValueError("Both entry_price and stop_loss_price must be provided.")

        if price_difference == 0:
            raise ValueError(
                f"Price difference cannot be zero. For entry price {signal.entry} and for stoploss {signal.stop_loss}"
            )

        position_size = risk_amount / price_difference

        return position_size
