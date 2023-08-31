import asyncio
import json
import websockets

from core.commands.broker import Subscribe
from core.event_decorators import command_handler
from core.events.ohlcv import NewMarketDataReceived
from core.models.timeframe import Timeframe
from core.models.ohlcv import OHLCV
from core.interfaces.abstract_ws import AbstractWS
from broker.retry import retry


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

    @retry(max_retries=5, initial_retry_delay=5, handled_exceptions=(Exception,))
    async def connect_to_websocket(self):
        self.ws = await websockets.connect(self.url)

    async def process_message(self, message):
        message_data = json.loads(message)

        if "topic" in message_data:
            ohlcv = message_data["data"][0]
            topic = message_data["topic"].split(".")
            symbol, interval = topic[2], topic[1]

            ohlcv_event = self.parse_candle_message(symbol, interval, ohlcv)

            await self.dispatch(ohlcv_event)

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)
            try:
                if self.ws.open:
                    await self.ws.ping()
                else:
                    raise websockets.exceptions.ConnectionClosedOK(None, websockets.frames.Close(code=1000, reason='Connection closed'))
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed.")
                await self.connect_to_websocket()
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed with error")
                await self.connect_to_websocket()
            except Exception as e:
                print(f"Error while keep alive ping: {e}")
                await self.connect_to_websocket()

    async def process_messages(self):
        while True:
            try:
                async for message in self.ws:
                    await self.process_message(message)
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed.")
                await self.connect_to_websocket()
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed with error")
                await self.connect_to_websocket()
            except Exception as e:
                print(f"Error while process message: {e}")
                await self.connect_to_websocket()

    async def run(self, ping_interval=10):
        try:
            await self.connect_to_websocket()

            ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))
            message_processing_task = asyncio.create_task(self.process_messages())

            await asyncio.gather(ping_task, message_processing_task)
        except ConnectionError as e:
            print(f"Could not establish WebSocket connection: {e}")
        finally:
            if self.ws:
                await self.ws.close()

    def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV.from_dict(data)
        return NewMarketDataReceived(symbol=symbol, timeframe=self.TIMEFRAMES[interval], ohlcv=ohlcv)


    @command_handler(Subscribe)
    async def subscribe(self, command: Subscribe):
        if self.ws is None:
            raise ValueError('Initialize ws')

        channels = [f"kline.{self.INTERVALS[timeframe]}.{symbol}" for (symbol, timeframe) in command.symbols_and_timeframes]

        for channel in channels:
            await self.ws.send(json.dumps({"op": "subscribe", "args": [channel]}))
