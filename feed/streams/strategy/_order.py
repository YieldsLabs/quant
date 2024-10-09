from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.entity.order import Order
from core.models.symbol import Symbol


class OrderStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWSExchange):
        await ws.auth()
        await ws.subscribe(ws.order_topic())

    async def unsubscribe(self, ws: AbstractWSExchange):
        await ws.unsubscribe(ws.order_topic())

    def parse(self, ws: AbstractWSExchange, topic, message):
        if topic != ws.order_topic():
            return []

        return [
            Order.from_dict(order)
            for order in message
            if order.get("symbol") == self.symbol.name
        ]
