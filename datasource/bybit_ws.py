
import asyncio
import json
import websockets
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.timeframe import Timeframe
from datasource.abstract_ws import AbstractWS


class BybitWSHandler(AbstractWS):
    INTERVALS = {
        Timeframe.ONE_MINUTE: 1,
        Timeframe.THREE_MINUTES: 3,
        Timeframe.FIVE_MINUTES: 5,
        Timeframe.FIFTEEN_MINUTES: 15,
        Timeframe.ONE_HOUR: 60,
        Timeframe.FOUR_HOURS: 240,
    }

    TIMEFRAMES = {
        '1': Timeframe.ONE_MINUTE,
        '3': Timeframe.THREE_MINUTES,
        '5': Timeframe.FIVE_MINUTES,
        '15': Timeframe.FIFTEEN_MINUTES,
        '60': Timeframe.ONE_HOUR,
        '240': Timeframe.FOUR_HOURS,
    }

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = None

    async def connect_to_websocket(self):
        while True:
            try:
                return await websockets.connect(self.url)
            except Exception as e:
                print(f"Failed to connect to websocket: {e}")
                await asyncio.sleep(1)

    async def process_message(self, message):
        message_data = json.loads(message)

        if "topic" in message_data:
            ohlcv = message_data["data"][0]
            topic = message_data["topic"].split(".")
            symbol, interval = topic[2], topic[1]

            ohlcv_event = self.parse_candle_message(symbol, interval, ohlcv)

            await self.dispatcher.dispatch(ohlcv_event)

    async def send_ping(self, interval):
        while True:
            try:
                await asyncio.sleep(interval)
                await self.ws.ping()
            except Exception as e:
                print(f"Unexpected error: {e}")

    async def process_messages(self):
        while True:
            try:
                async for message in self.ws:
                    await self.process_message(message)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Websocket closed with code {e.code}: {e.reason}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    async def run(self, ping_interval=10):
        self.ws = await self.connect_to_websocket()

        ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))
        message_processing_task = asyncio.create_task(self.process_messages())

        try:
            await asyncio.gather(ping_task, message_processing_task)
        finally:
            ping_task.cancel()
            message_processing_task.cancel()

    def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV(
            timestamp=int(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"]),
        )

        return OHLCVEvent(symbol=symbol, timeframe=self.TIMEFRAMES[interval], ohlcv=ohlcv)

    async def subscribe(self, timeframes_and_symbols):
        if self.ws is None:
            raise ValueError('Initialize ws')

        channels = [f"kline.{self.INTERVALS[timeframe]}.{symbol}" for (symbol, timeframe) in timeframes_and_symbols]

        for channel in channels:
            await self.ws.send(json.dumps({"op": "subscribe", "args": [channel]}))
