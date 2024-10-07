from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class LiquidationStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWS):
        await ws.subscribe(ws.liquidation_topic(self.symbol))

    async def unsubscribe(self, ws: AbstractWS):
        await ws.unsubscribe(ws.liquidation_topic(self.symbol))

    def parse(self, message):
        return [message]
