from typing import Type
from broker.abstract_broker import AbstractBroker
from core.event_dispatcher import register_handler
from core.events.order import FillOrder, Order, OrderSide
from core.events.position import ClosePosition, ClosedPosition, OpenLongPosition, OpenShortPosition, PositionSide
from trader.abstract_trader import AbstractTrader

class SimpleTrader(AbstractTrader):
    def __init__(self, broker: Type[AbstractBroker]):
        super().__init__()
        self.broker = broker

    @register_handler(OpenLongPosition)
    def _open_long_position(self, event: OpenLongPosition):
        self.trade(event)

    @register_handler(OpenShortPosition)
    def _open_short_position(self, event: OpenShortPosition):
        self.trade(event)

    @register_handler(ClosePosition)
    def _on_close_position(self, event: ClosePosition):
        self.broker.close_position(event.symbol)
        self.dispatcher.dispatch(ClosedPosition(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.exit_price))

    def trade(self, event):
        order_side = OrderSide.BUY if isinstance(event, OpenLongPosition) else OrderSide.SELL
        
        order_params = {
            "symbol": event.symbol,
            "order_side": order_side,
            "entry_price": event.entry,
            "position_size": event.size,
            "stop_loss_price": event.stop_loss,
            "take_profit_price": event.take_profit
        }

        current_order_id = self.broker.place_limit_order(**order_params)

        if not current_order_id:
            return

        order = Order(id=current_order_id, side=order_side, size=event.size, entry=event.entry, stop_loss=event.stop_loss, take_profit=event.take_profit)
        
        self.dispatcher.dispatch(FillOrder(symbol=event.symbol, timeframe=event.timeframe, order=order))