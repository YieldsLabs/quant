from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class OrderBookStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol, depth: int):
        super().__init__()
        self.symbol = symbol
        self.depth = depth

    async def subscribe(
        self,
        ws: AbstractWS,
    ):
        await ws.subscribe(ws.order_book_topic(self.symbol, self.depth))

    async def unsubscribe(
        self,
        ws: AbstractWS,
    ):
        await ws.unsubscribe(ws.order_book_topic(self.symbol, self.depth))

    def parse(self, message):
        return message
