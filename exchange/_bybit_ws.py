import asyncio
import json
import logging
import time

import websockets
from websockets.exceptions import ConnectionClosedError

from core.models.bar import Bar
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


def debounce(period):
    def decorator(f):
        async def wrapped(*args, **kwargs):
            now = time.time()
            delay = 0.0
            if wrapped.last_call_time is not None:
                timedelta = now - wrapped.last_call_time
                if 0 <= timedelta <= period:
                    delay = abs(period - timedelta)
            await asyncio.sleep(delay)
            wrapped.last_call_time = time.time()
            await f(*args, **kwargs)

        wrapped.last_call_time = None
        return wrapped

    return decorator


class BybitWS:
    _instance = None

    SUBSCRIBE_OPERATION = "subscribe"
    UNSUBSCRIBE_OPERATION = "unsubscribe"
    INTERVALS = {
        Timeframe.ONE_MINUTE: 1,
        Timeframe.THREE_MINUTES: 3,
        Timeframe.FIVE_MINUTES: 5,
        Timeframe.FIFTEEN_MINUTES: 15,
        Timeframe.ONE_HOUR: 60,
        Timeframe.FOUR_HOURS: 240,
    }

    KLINE_CHANNEL = "kline"
    TOPIC_KEY = "topic"
    DATA_KEY = "data"
    CONFIRM_KEY = "confirm"

    def __new__(cls, wss: str):
        if cls._instance is None:
            cls._instance = super(BybitWS, cls).__new__(cls)
            cls._instance.ws = None
            cls._instance.wss = wss
            cls._instance._channels = set()
            cls._instance._receive_semaphore = asyncio.Semaphore(1)
            cls._instance._lock = asyncio.Lock()
            cls._instance.ping_task = None

        return cls._instance

    async def connect_to_websocket(self, interval=5):
        if self.ws and self.ws.open:
            return

        self.ws = await websockets.connect(self.wss)

        await asyncio.sleep(interval)

        if not self.ws.open:
            raise RuntimeError("Reconnect WS")

        await self._resubscribe()

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)

            if not self.ws or not self.ws.open:
                continue

            pong = await self.ws.ping()
            await pong

    @retry(
        max_retries=8,
        initial_retry_delay=1,
        handled_exceptions=(ConnectionError, RuntimeError, ConnectionClosedError),
    )
    async def run(self, ping_interval=15):
        await self.connect_to_websocket()

        if not self.ping_task:
            self.ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))

    async def close(self):
        if self.ws and self.ws.open:
            await self.ws.close()

        self.ping_task.cancel()
        self.ping_task = None

    async def receive(self, interval=5):
        async with self._receive_semaphore:
            if not self.ws or not self.ws.open:
                await asyncio.sleep(interval)
                return

            async for message in self.ws:
                data = json.loads(message)

                if self.TOPIC_KEY in data:
                    ohlcv = data[self.DATA_KEY][0]

                    return Bar(OHLCV.from_dict(ohlcv), ohlcv[self.CONFIRM_KEY])

    async def subscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) not in self._channels:
                self._channels.add((symbol, timeframe))
                await self._subscribe(symbol, timeframe)

    @debounce(5)
    async def _subscribe(self, symbol, timeframe):
        if not self.ws or not self.ws.open:
            return

        channel = f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
        subscribe_message = {"op": self.SUBSCRIBE_OPERATION, "args": [channel]}

        try:
            await self.ws.send(json.dumps(subscribe_message))
        except Exception as e:
            logger.error(e)

    async def _resubscribe(self):
        async with self._lock:
            for symbol, timeframe in self._channels:
                await self._subscribe(symbol, timeframe)
