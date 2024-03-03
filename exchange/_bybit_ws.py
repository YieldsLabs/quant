import asyncio
import json
import logging
from asyncio.exceptions import CancelledError

import websockets
from websockets.exceptions import ConnectionClosedError

from core.interfaces.abstract_ws import AbstractWS
from core.models.bar import Bar
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


class BybitWS(AbstractWS):
    _instance = None

    SUBSCRIBE_OPERATION = "subscribe"
    UNSUBSCRIBE_OPERATION = "unsubscribe"
    PING_OPERATION = "ping"
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
            cls.ping_task = None

        return cls._instance

    async def _connect_to_websocket(self):
        self.ws = await websockets.connect(
            self.wss,
            open_timeout=2,
            ping_interval=20,
            ping_timeout=10,
            close_timeout=1,
        )

        if not self.ws.open:
            raise RuntimeError("Reconnect WS")

        await self._resubscribe()

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
    async def run(self):
        await self.close()
        await self._connect_to_websocket()

    async def close(self):
        if self.ws and self.ws.open:
            await self.ws.close()

    @retry(
        max_retries=13,
        initial_retry_delay=5,
        handled_exceptions=(RuntimeError, ConnectionClosedError),
    )
    async def receive(self, symbol, timeframe):
        async with self._receive_semaphore:
            if not self.ws or not self.ws.open:
                await self._connect_to_websocket()

            async for message in self.ws:
                data = json.loads(message)

                if self.TOPIC_KEY not in data:
                    return

                topic = data["topic"].split(".")

                if symbol.name == topic[2] and timeframe == self.TIMEFRAMES[topic[1]]:
                    ohlcv = data[self.DATA_KEY][0]

                    return Bar(OHLCV.from_dict(ohlcv), ohlcv[self.CONFIRM_KEY])

    async def subscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) not in self._channels:
                self._channels.add((symbol, timeframe))
                await self._subscribe(symbol, timeframe)

    async def unsubscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) in self._channels:
                self._channels.remove((symbol, timeframe))
                await self._unsubscribe(symbol, timeframe)

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

    async def _unsubscribe(self, symbol, timeframe):
        if not self.ws or not self.ws.open:
            return

        channel = f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
        unsubscribe_message = {"op": self.UNSUBSCRIBE_OPERATION, "args": [channel]}

        try:
            logger.info(f"Unsubscribe from: {unsubscribe_message}")
            await self.ws.send(json.dumps(unsubscribe_message))
        except Exception as e:
            logger.error(e)

    async def _resubscribe(self):
        async with self._lock:
            for symbol, timeframe in self._channels:
                await self._subscribe(symbol, timeframe)
