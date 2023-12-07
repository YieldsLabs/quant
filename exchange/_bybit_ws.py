import asyncio
import json
import logging

import websockets
from websockets.exceptions import ConnectionClosedError

from core.interfaces.abstract_ws import AbstractWS
from core.models.bar import Bar
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


class BybitWS(AbstractWS):
    SUBSCRIBE_OPERATION = "subscribe"
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

    _instance = None

    def __new__(cls, wss: str):
        if not cls._instance:
            cls._instance = super(BybitWS, cls).__new__(cls)
            cls._instance._initialize(wss)
        return cls._instance

    def _initialize(self, wss: str):
        self.ws = None
        self.wss = wss
        self._channels = []

    async def connect_to_websocket(self, interval=15):
        await self.close()

        self.ws = await websockets.connect(self.wss)

        await asyncio.sleep(interval)

        if not self.ws.open:
            raise RuntimeError("Reconnect WS")

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)

            if not self.ws:
                continue

            if not self.ws.open:
                continue

            pong = await self.ws.ping()
            await pong

    @retry(
        max_retries=8,
        initial_retry_delay=1,
        handled_exceptions=(ConnectionError, RuntimeError, ConnectionClosedError),
    )
    async def run(self, ping_interval=15):
        try:
            await self.connect_to_websocket()
            await self._subscribe()

            ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))

            done, pending = await asyncio.wait(
                [ping_task],
                return_when=asyncio.FIRST_EXCEPTION,
            )

            for task in pending:
                task.cancel()

            for task in done:
                if task.exception():
                    raise task.exception()

        except Exception as e:
            logger.error(e)
        finally:
            raise RuntimeError("WS Message Error")

    async def close(self):
        if self.ws and self.ws.open:
            await self.ws.close()

    async def receive(self):
        if not self.ws or not self.ws.open:
            return

        message = await self.ws.recv()
        data = json.loads(message)

        if self.TOPIC_KEY not in data:
            return

        ohlcv = data[self.DATA_KEY][0]

        return Bar(OHLCV.from_dict(ohlcv), ohlcv[self.CONFIRM_KEY])

    async def subscribe(self, symbol, timeframe):
        channel = f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
        self._channels = list(set(self._channels + [channel]))
        await self._subscribe()

    async def _subscribe(self):
        if not self.ws or not self.ws.open:
            return

        for channel in self._channels:
            subscribe_message = {"op": self.SUBSCRIBE_OPERATION, "args": [channel]}

            try:
                await self.ws.send(json.dumps(subscribe_message))
            except Exception as e:
                logger.error(e)
