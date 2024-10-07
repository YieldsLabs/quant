from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class OrderStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWS):
        await ws.auth()
        await ws.subscribe(ws.order_topic())

    async def unsubscribe(self, ws: AbstractWS):
        await ws.unsubscribe(ws.order_topic())

    def parse(self, message):
        return [order for order in message if order.get("symbol") == self.symbol.name]
