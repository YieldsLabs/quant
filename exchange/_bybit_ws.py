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

    async def _connect(self):
        if not self.ws or not self.ws.open:
            try:
                self.ws = await websockets.connect(
                    self.wss,
                    open_timeout=2,
                    ping_interval=18,
                    ping_timeout=10,
                    close_timeout=3,
                )

                await self._wait_for_ws()
                await self._subscribe()

                logger.info("WebSocket connection established.")
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket: {e}")
                raise ConnectionError(e)

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=(ConnectionError, ConnectionClosedError),
    )
    async def run(self):
        await self.close()
        await self._connect()

    async def close(self):
        if self.ws and self.ws.open:
            await self._unsubscribe()
            await self.ws.close()
            await self.ws.wait_closed()

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=(
            ConnectionError,
            ConnectionClosedError,
        ),
    )
    async def receive(self, symbol, timeframe):
        await self._connect()

        async for message in self.ws:
            try:
                data = json.loads(message)

                if not self._is_valid_message(symbol, timeframe, data):
                    continue

                return self._parse_ohlcv(data)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Malformed message received: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while receiving message: {e}")

    async def subscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) not in self._channels:
                self._channels.add((symbol, timeframe))
                await self._subscribe()

    async def unsubscribe(self, symbol, timeframe):
        async with self._lock:
            if (symbol, timeframe) in self._channels:
                self._channels.remove((symbol, timeframe))
                await self._subscribe()

    async def _subscribe(self):
        if not self.ws or not self.ws.open:
            return

        subscribe_message = {
            "op": self.SUBSCRIBE_OPERATION,
            "args": self._get_channels_args(),
        }

        try:
            logger.info(f"Subscribe to: {subscribe_message}")
            await self.ws.send(json.dumps(subscribe_message))
        except Exception as e:
            logger.error(f"Failed to send subscribe message: {e}")

    async def _unsubscribe(self):
        if not self.ws or not self.ws.open or not self._channels:
            return

        unsubscribe_message = {
            "op": self.UNSUBSCRIBE_OPERATION,
            "args": self._get_channels_args(),
        }

        try:
            logger.info(f"Unsubscribe from: {unsubscribe_message}")
            await self.ws.send(json.dumps(unsubscribe_message))
        except Exception as e:
            logger.error(f"Failed to send unsubscribe message: {e}")

    async def _wait_for_ws(self):
        while not self.ws or not self.ws.open:
            await asyncio.sleep(1.0)

    def _is_valid_message(self, symbol, timeframe, data):
        if self.TOPIC_KEY not in data:
            return False

        topic = data[self.TOPIC_KEY].split(".")

        return symbol.name == topic[2] and timeframe == self.TIMEFRAMES.get(topic[1])

    def _parse_ohlcv(self, data):
        return [
            Bar(OHLCV.from_dict(ohlcv), ohlcv.get(self.CONFIRM_KEY))
            for ohlcv in data.get(self.DATA_KEY, [])
            if ohlcv
        ]

    def _get_channels_args(self):
        return [
            f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol.name}"
            for symbol, timeframe in self._channels
        ]
