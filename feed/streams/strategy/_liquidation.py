from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.symbol import Symbol


class LiquidationStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol
        self.topic = None

    async def subscribe(self, ws: AbstractWSExchange):
        self.topic = ws.liquidation_topic(self.symbol)
        await ws.subscribe(self.topic)

    async def unsubscribe(self, ws: AbstractWSExchange):
        if self.topic:
            await ws.unsubscribe(self.topic)
            self.topic = None

    async def next(self, ws: AbstractWSExchange):
        if not self.topic:
            return []

        message = await ws.get_message(self.topic)

        return [message]
