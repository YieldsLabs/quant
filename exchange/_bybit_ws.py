import asyncio
import json
import logging
from asyncio.exceptions import CancelledError

import websockets
from websockets.exceptions import ConnectionClosedError

from core.models.bar import Bar
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


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

    TIMEFRAMES = {
        "1": Timeframe.ONE_MINUTE,
        "3": Timeframe.THREE_MINUTES,
        "5": Timeframe.FIVE_MINUTES,
        "15": Timeframe.FIFTEEN_MINUTES,
        "60": Timeframe.ONE_HOUR,
        "240": Timeframe.FOUR_HOURS,
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
            try:
                await asyncio.sleep(interval)

                if not self.ws or not self.ws.open:
                    continue

                await asyncio.wait_for(self.ws.ping(), timeout=interval)
            except Exception as e:
                logger.error(e)
                self.ping_task = None
                raise e

    @retry(
        max_retries=13,
        initial_retry_delay=3,
        handled_exceptions=(
            ConnectionError,
            RuntimeError,
            ConnectionClosedError,
            CancelledError,
        ),
    )
    async def run(self, ping_interval=5):
        await self.connect_to_websocket()

        if not self.ping_task:
            self.ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))

    async def close(self):
        if self.ws and self.ws.open:
            await self.ws.close()

        if self.ping_task:
            self.ping_task.cancel()

        self.ping_task = None

    @retry(
        max_retries=13,
        initial_retry_delay=5,
        handled_exceptions=(RuntimeError, ConnectionClosedError),
    )
    async def receive(self, symbol, timeframe):
        async with self._receive_semaphore:
            if not self.ws or not self.ws.open:
                await self.connect_to_websocket()

            async for message in self.ws:
                data = json.loads(message)

                if self.TOPIC_KEY not in data:
                    return

                topic = data["topic"].split(".")
                _symbol, _timeframe = topic[2], topic[1]

                if symbol.name == _symbol and timeframe == self.TIMEFRAMES[_timeframe]:
                    ohlcv = data[self.DATA_KEY][0]

                    return Bar(OHLCV.from_dict(ohlcv), ohlcv[self.CONFIRM_KEY])

    async def subscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) not in self._channels:
                self._channels.add((symbol, timeframe))
                await self._subscribe(symbol, timeframe)

    async def _subscribe(self, symbol, timeframe):
        if not self.ws or not self.ws.open:
            return

        channel = f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
        subscribe_message = {"op": self.SUBSCRIBE_OPERATION, "args": [channel]}

        try:
            logger.info(f"Subscribe to: {subscribe_message}")
            await self.ws.send(json.dumps(subscribe_message))
        except Exception as e:
            logger.error(e)

    async def _resubscribe(self):
        async with self._lock:
            for symbol, timeframe in self._channels:
                await self._subscribe(symbol, timeframe)
