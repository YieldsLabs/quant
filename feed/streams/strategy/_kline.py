from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class KlineStreamStrategy(AbstractStreamStrategy):
    def __init__(self, timeframe: Timeframe, symbol: Symbol):
        super().__init__()
        self.timeframe = timeframe
        self.symbol = symbol

    async def subscribe(self, ws: AbstractWS):
        await ws.subscribe(ws.kline_topic(self.timeframe, self.symbol))

    async def unsubscribe(self, ws: AbstractWS):
        await ws.unsubscribe(ws.kline_topic(self.timeframe, self.symbol))

    def parse(self, message):
        return [
            Bar(OHLCV.from_dict(ohlcv), ohlcv.get("confirm", False))
            for ohlcv in message
        ]
