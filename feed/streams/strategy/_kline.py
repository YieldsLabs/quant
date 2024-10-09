from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class KlineStreamStrategy(AbstractStreamStrategy):
    def __init__(self, timeframe: Timeframe, symbol: Symbol):
        super().__init__()
        self.timeframe = timeframe
        self.symbol = symbol
        self.topic = None

    async def subscribe(self, ws: AbstractWSExchange):
        self.topic = ws.kline_topic(self.timeframe, self.symbol)
        await ws.subscribe(self.topic)

    async def unsubscribe(self, ws: AbstractWSExchange):
        if self.topic:
            await ws.unsubscribe(self.topic)
            self.topic = None

    async def next(self, ws: AbstractWSExchange):
        if not self.topic:
            return []

        message = await ws.get_message(self.topic)

        return [
            Bar(OHLCV.from_dict(ohlcv), ohlcv.get("confirm", False))
            for ohlcv in message
        ]
