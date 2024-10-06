from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class OrderBookStreamStrategy(AbstractStreamStrategy):
    def __init__(self, ws: AbstractWS, symbol: Symbol, depth: int):
        super().__init__()
        self.ws = ws
        self.symbol = symbol
        self.topic = ws.order_book_topic(symbol, depth)

    async def subscribe(self):
        await self.ws.subscribe(self.topic)

    async def unsubscribe(self):
        await self.ws.unsubscribe(self.topic)

    def parse(self, message):
        return message
