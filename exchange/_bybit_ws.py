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

    def __init__(self, wss: str):
        self.wss = wss
        self.ws = None
        self._channels = set()
        self._lock = asyncio.Lock()

    async def _connect_to_websocket(self):
        if not self.ws or not self.ws.open:
            self.ws = await websockets.connect(
                self.wss,
                open_timeout=None,
                ping_interval=18,
                ping_timeout=10,
                close_timeout=None,
            )

    @retry(
        max_retries=13,
        initial_retry_delay=1,
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
        await self._subscribe()

    async def close(self):
        if self.ws and self.ws.open:
            await self.ws.close()

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=(RuntimeError, ConnectionClosedError),
    )
    async def receive(self, symbol, timeframe):
        await self._connect_to_websocket()

        async for message in self.ws:
            data = json.loads(message)

            if self.TOPIC_KEY not in data:
                continue

            topic = data[self.TOPIC_KEY].split(".")

            if symbol.name == topic[2] and timeframe == self.TIMEFRAMES.get(topic[1]):
                return [
                    Bar(OHLCV.from_dict(ohlcv), ohlcv.get(self.CONFIRM_KEY))
                    for ohlcv in data.get(self.DATA_KEY, None)
                    if ohlcv
                ]

    async def subscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) not in self._channels:
                self._channels.add((symbol, timeframe))
                await self._subscribe()

    async def unsubscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) in self._channels:
                self._channels.remove((symbol, timeframe))
                await self._unsubscribe()

    async def _subscribe(self):
        if not self.ws or not self.ws.open:
            return

        channels = [
            f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
            for symbol, timeframe in self._channels
        ]
        subscribe_message = {"op": self.SUBSCRIBE_OPERATION, "args": channels}

        try:
            logger.info(f"Subscribe to: {subscribe_message}")
            await self.ws.send(json.dumps(subscribe_message))
        except Exception as e:
            logger.error(f"Failed to send subscribe message: {e}")

    async def _unsubscribe(self):
        if not self.ws or not self.ws.open:
            return

        channels = [
            f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
            for symbol, timeframe in self._channels
        ]
        unsubscribe_message = {"op": self.UNSUBSCRIBE_OPERATION, "args": channels}

        try:
            logger.info(f"Unsubscribe from: {unsubscribe_message}")
            await self.ws.send(json.dumps(unsubscribe_message))
        except Exception as e:
            logger.error(f"Failed to send unsubscribe message: {e}")
