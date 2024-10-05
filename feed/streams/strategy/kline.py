from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class KlineStreamStrategy(AbstractStreamStrategy):
    def __init__(self, ws: AbstractWS, timeframe: Timeframe, symbol: Symbol):
        self.ws = ws
        self.timeframe = timeframe
        self.symbol = symbol
        self.kline_topic = ws.kline_topic(timeframe, symbol)

    async def subscribe(self):
        await self.ws.subscribe(self.kline_topic)

    async def unsubscribe(self):
        await self.ws.unsubscribe(self.kline_topic)

    def parse(self, message):
        return [Bar(OHLCV.from_dict(ohlcv), confirm) for ohlcv, confirm in message]
