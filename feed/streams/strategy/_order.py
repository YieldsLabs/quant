from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class OrderStreamStrategy(AbstractStreamStrategy):
    def __init__(self, ws: AbstractWS, symbol: Symbol):
        super().__init__()
        self.ws = ws
        self.symbol = symbol
        self.topic = ws.order_topic()

    async def subscribe(self):
        await self.ws.auth()
        await self.ws.subscribe(self.topic)

    async def unsubscribe(self):
        await self.ws.unsubscribe(self.topic)

    def parse(self, message):
        return [order for order in message if order.get("symbol") == self.symbol.name]
