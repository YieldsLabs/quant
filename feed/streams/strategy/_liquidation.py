from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.symbol import Symbol


class LiquidationStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWSExchange):
        await ws.subscribe(ws.liquidation_topic(self.symbol))

    async def unsubscribe(self, ws: AbstractWSExchange):
        await ws.unsubscribe(ws.liquidation_topic(self.symbol))

    def parse(self, ws: AbstractWSExchange, topic: str, message):
        if topic != ws.liquidation_topic(self.symbol):
            return []

        return [message]
