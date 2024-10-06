from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class KlineStreamStrategy(AbstractStreamStrategy):
    def __init__(self, ws: AbstractWS, timeframe: Timeframe, symbol: Symbol):
        super().__init__()
        self.ws = ws
        self.timeframe = timeframe
        self.symbol = symbol
        self.topic = ws.kline_topic(timeframe, symbol)

    async def subscribe(self):
        await self.ws.subscribe(self.topic)

    async def unsubscribe(self):
        await self.ws.unsubscribe(self.topic)

    def parse(self, message):
        return [
            Bar(OHLCV.from_dict(ohlcv), ohlcv.get("confirm", False))
            for ohlcv in message
        ]
