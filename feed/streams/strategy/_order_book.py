from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.symbol import Symbol


class OrderBookStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol, depth: int):
        super().__init__()
        self.symbol = symbol
        self.depth = depth

    async def subscribe(
        self,
        ws: AbstractWSExchange,
    ):
        await ws.subscribe(ws.order_book_topic(self.symbol, self.depth))

    async def unsubscribe(
        self,
        ws: AbstractWSExchange,
    ):
        await ws.unsubscribe(ws.order_book_topic(self.symbol, self.depth))

    def parse(self, ws: AbstractWSExchange, topic, message):
        if topic != ws.order_book_topic(self.symbol, self.depth):
            return

        return message
