from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class LiquidationStreamStrategy(AbstractStreamStrategy):
    def __init__(self, ws: AbstractWS, symbol: Symbol):
        super().__init__()
        self.ws = ws
        self.symbol = symbol
        self.topic = ws.liquidation_topic(symbol)

    async def subscribe(self):
        await self.ws.subscribe(self.topic)

    async def unsubscribe(self):
        await self.ws.unsubscribe(self.topic)

    def parse(self, message):
        return message
