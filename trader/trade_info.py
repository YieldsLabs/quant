from dataclasses import dataclass

from shared.position_side import PositionSide

@dataclass
class TradeInfo:
    position_side: PositionSide
    entry_price: float
    position_size: float
    stop_loss_price: float
    take_profit_price: float
    current_order_id: str = None