from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.symbol import Symbol


class OrderBookStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol, depth: int):
        super().__init__()
        self.symbol = symbol
        self.depth = depth
        self.topic = None

    async def subscribe(
        self,
        ws: AbstractWSExchange,
    ):
        self.topic = ws.order_book_topic(self.symbol, self.depth)
        await ws.subscribe(self.topic)

    async def unsubscribe(
        self,
        ws: AbstractWSExchange,
    ):
        if self.topic:
            await ws.unsubscribe(self.topic)
            self.topic = None

    async def next(self, ws: AbstractWSExchange):
        if not self.topic:
            return []

        message = await ws.get_message(self.topic)

        return [message]
