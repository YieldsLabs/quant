import asyncio
import json
import logging

import websockets
from websockets.exceptions import ConnectionClosedError

from core.commands.broker import Subscribe
from core.event_decorators import command_handler
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_ws import AbstractWS
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


class BybitWSHandler(AbstractWS):
    INTERVALS = {
        Timeframe.ONE_MINUTE: 1,
        Timeframe.THREE_MINUTES: 3,
        Timeframe.FIVE_MINUTES: 5,
        Timeframe.FIFTEEN_MINUTES: 15,
        Timeframe.ONE_HOUR: 60,
        Timeframe.FOUR_HOURS: 240,
    }

    TIMEFRAMES = {str(v): k for k, v in INTERVALS.items()}

    SUBSCRIBE_OPERATION = "subscribe"
    KLINE_CHANNEL = "kline"
    TOPIC_KEY = "topic"
    DATA_KEY = "data"
    CONFIRM_KEY = "confirm"

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.ws = None

    @retry(
        max_retries=5,
        initial_retry_delay=5,
        handled_exceptions=(ConnectionError, ConnectionClosedError),
    )
    async def connect_to_websocket(self):
        self.ws = await websockets.connect(self.url)

    async def process_message(self, message):
        message_data = json.loads(message)

        if self.TOPIC_KEY in message_data:
            ohlcv = message_data[self.DATA_KEY][0]
            topic = message_data[self.TOPIC_KEY].split(".")
            symbol, interval = topic[2], topic[1]

            if interval not in self.TIMEFRAMES:
                logger.error(f"Unknown interval: {interval}")
                return None

            ohlcv_event = self.parse_candle_message(symbol, interval, ohlcv)

            if ohlcv[self.CONFIRM_KEY]:
                logger.info(f"Tick: {symbol}:{interval}:{ohlcv_event}")

            await self.dispatch(ohlcv_event)

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)

            if not self.ws:
                continue

            if self.ws.open:
                await self.ws.ping()
            else:
                logger.info("WebSocket not open, attempting to reconnect...")
                await self.connect_to_websocket()

    async def process_messages(self):
        while True:
            message = await self.ws.recv()

            if message is None:
                break

            await self.process_message(message)

    async def run(self, ping_interval=10):
        try:
            await self.connect_to_websocket()

            ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))
            message_processing_task = asyncio.create_task(self.process_messages())
            
            done, pending = await asyncio.wait(
                [ping_task, message_processing_task], return_when=asyncio.FIRST_EXCEPTION
            )

            for task in pending:
                task.cancel()

            for task in done:
                if task.exception():
                    logger.error(f"Task raised an exception: {task.exception()}")
        finally:
            if self.ws:
                await self.ws.close()

    def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV.from_dict(data)
        return NewMarketDataReceived(
            symbol, self.TIMEFRAMES[interval], ohlcv, data[self.CONFIRM_KEY]
        )

    @command_handler(Subscribe)
    async def subscribe(self, command: Subscribe):
        if not self.ws or not self.ws.open:
            raise ValueError("WebSocket is not connected or open.")

        channels = [
            f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol}"
            for symbol, timeframe in command.symbols_and_timeframes
        ]

        subscribe_message = json.dumps(
            {"op": self.SUBSCRIBE_OPERATION, "args": channels}
        )
        await self.ws.send(subscribe_message)
