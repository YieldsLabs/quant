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

    async def subscribe(self, ws: AbstractWSExchange):
        await ws.subscribe(ws.kline_topic(self.timeframe, self.symbol))

    async def unsubscribe(self, ws: AbstractWSExchange):
        await ws.unsubscribe(ws.kline_topic(self.timeframe, self.symbol))

    def parse(self, ws: AbstractWSExchange, topic: str, message):
        if topic != ws.kline_topic(self.timeframe, self.symbol):
            return []

        return [
            Bar(OHLCV.from_dict(ohlcv), ohlcv.get("confirm", False))
            for ohlcv in message
        ]
