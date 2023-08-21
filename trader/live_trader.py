from typing import Type, Union
import logging

from broker.abstract_broker import AbstractBroker
from core.event_decorators import register_handler
from core.events.position import PositionClosed, LongPositionOpened, ShortPositionOpened, ClosePositionPrepared, OrderFilled
from core.position import Order, OrderSide

from .abstract_trader import AbstractTrader


class LiveTrader(AbstractTrader):
    def __init__(self, broker: Type[AbstractBroker]):
        super().__init__()
        self.broker = broker
        self.logger = logging.getLogger(__name__)

    @register_handler(LongPositionOpened)
    async def _open_long_position(self, event: LongPositionOpened):
        await self.trade(event)

    @register_handler(ShortPositionOpened)
    async def _open_short_position(self, event: ShortPositionOpened):
        await self.trade(event)

    @register_handler(ClosePositionPrepared)
    async def _on_close_position(self, event: ClosePositionPrepared):
        self.broker.close_position(event.symbol)

        await self.dispatcher.dispatch(
            PositionClosed(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.exit_price))

    async def trade(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL

        order_params = {
            "symbol": event.symbol,
            "side": order_side,
            "position_size": event.size
        }

        try:
            current_order_id = self.broker.place_market_order(**order_params)
            position = self.broker.get_open_position(event.symbol)

            order = Order(id=current_order_id, side=order_side, size=position['position_size'], price=position['entry_price'])

            await self.dispatcher.dispatch(
                OrderFilled(symbol=event.symbol, timeframe=event.timeframe, order=order))
        except Exception as e:
            self.logger.error(f"Error placing order for {event.symbol}: {e}")
            await self.dispatcher.dispatch(
                PositionClosed(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.entry))
