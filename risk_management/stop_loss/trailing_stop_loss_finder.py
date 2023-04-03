from typing import Type
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from shared.ohlcv_context import OhlcvContext
from shared.position_side import PositionSide

class TrailingStopLossFinder(AbstractStopLoss):
    def __init__(self, ohlcv: Type[OhlcvContext], stop_loss_finder: Type[AbstractStopLoss], risk_reward_ratio=1.1, max_adjustments=20):
        super().__init__(ohlcv)
        self.stop_loss_finder = stop_loss_finder
        self.risk_reward_ratio = risk_reward_ratio
        self.max_adjustments = max_adjustments
        self.reset()

    def next(self, position_side, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')
        
        self.current_stop_loss[position_side.value] = self.stop_loss_finder.next(position_side, entry_price)
        self.adjustments[position_side.value] = 0

        while True:
            current_row = data.iloc[-1]
            adjusted_stop_loss = self._adjust_stop_loss(current_row, position_side, entry_price)
            if adjusted_stop_loss:
                print(f'Trade {position_side.value}, Current stop_loss={self.current_stop_loss[position_side.value]}, Adjusted stop_loss={adjusted_stop_loss}')
                self.current_stop_loss[position_side.value] = adjusted_stop_loss
                self.adjustments[position_side.value] += 1
            else:
                break

            if self.adjustments[position_side.value] >= self.max_adjustments:
                break

        return self.current_stop_loss[position_side.value]

    def _adjust_stop_loss(self, current_row, position_side, entry_price):
        current_price = current_row['close']

        risk = abs(entry_price - self.current_stop_loss[position_side.value])
        reward = abs(current_price - entry_price)
        
        risk_reward = risk / reward if reward != 0 else 0

        if position_side == PositionSide.LONG and risk_reward > self.risk_reward_ratio:
            new_stop_loss = max(entry_price, self.stop_loss_finder.next(position_side, entry_price))
        elif position_side == PositionSide.SHORT and risk_reward > self.risk_reward_ratio:
            new_stop_loss = min(entry_price, self.stop_loss_finder.next(position_side, entry_price))
        else:
            return
        
        if new_stop_loss >= self.current_stop_loss[position_side.value]:
            return None
        
        return new_stop_loss

    def reset(self):
        self.stop_loss_finder.reset()
        self.current_stop_loss = { PositionSide.LONG.value: None, PositionSide.SHORT.value: None }
        self.adjustments = { PositionSide.LONG.value: 0, PositionSide.SHORT.value: 0 }
    
    def __str__(self) -> str:
        return f'TrailingStopLossFinder(stop_loss_finder={self.stop_loss_finder})'

