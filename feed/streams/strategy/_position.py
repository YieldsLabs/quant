from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol


class PositionStreamStrategy(AbstractStreamStrategy):
    def __init__(self, symbol: Symbol):
        super().__init__()
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWS):
        await ws.auth()
        await ws.subscribe(ws.position_topic())

    async def unsubscribe(self, ws: AbstractWS):
        await ws.unsubscribe(ws.position_topic())

    def parse(self, message):
        return [
            position
            for position in message
            if position.get("symbol") == self.symbol.name
        ]
