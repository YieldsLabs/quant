import asyncio
import json
import logging

import websockets
from websockets.exceptions import ConnectionClosedError

from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)

connect_exceptions = (ConnectionError, ConnectionClosedError, asyncio.TimeoutError)


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

    TOPIC_KEY = "topic"
    DATA_KEY = "data"
    CONFIRM_KEY = "confirm"

    def __init__(self, wss: str):
        self.wss = wss
        self.ws = None
        self._lock = asyncio.Lock()
        self.subscriptions = []

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

                await self._wait_for_ws(timeout=5)
                logger.info("WebSocket connection established.")
                await self._resubscribe_all()
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket: {e}")
                raise ConnectionError("Failed to connect to WebSocket") from None

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=connect_exceptions,
    )
    async def connect(self):
        await self.close()
        await self._connect()

    async def close(self):
        if self.ws:
            await self.ws.close()
            await self.ws.wait_closed()

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=connect_exceptions,
    )
    async def receive(self):
        await self._connect()

        async for message in self.ws:
            try:
                data = json.loads(message)

                if not self._is_valid_message(data):
                    continue

                if self.DATA_KEY in data:
                    ohlcv_data = [
                        (ohlcv, ohlcv.get(self.CONFIRM_KEY, False))
                        for ohlcv in data[self.DATA_KEY]
                        if ohlcv
                    ]

                    if ohlcv_data:
                        yield ohlcv_data
                else:
                    yield []
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Malformed message received: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while receiving message: {e}")

    async def subscribe(self, topic: str):
        await self._send(self.SUBSCRIBE_OPERATION, [topic])
        self.subscriptions.append(topic)

    async def unsubscribe(self, topic):
        await self._send(self.UNSUBSCRIBE_OPERATION, [topic])

        if topic in self.subscriptions:
            self.subscriptions.remove(topic)

    def kline_topic(self, timeframe: Timeframe, symbol: Symbol) -> str:
        return f"kline.{self.INTERVALS[timeframe]}.{symbol.name}"

    async def _send(self, operation, args, timeout=5):
        if not self.ws or not self.ws.open:
            return

        message = {
            "op": operation,
            "args": args,
        }

        try:
            await asyncio.wait_for(self.ws.send(json.dumps(message)), timeout=timeout)

            logger.info(f"{operation.capitalize()} to: {message}")
        except asyncio.TimeoutError:
            logger.error("Subscription request timed out")
        except Exception as e:
            logger.error(f"Failed to send {operation} message: {e}")

    async def _wait_for_ws(self, timeout=10):
        try:
            await asyncio.wait_for(self._check_ws_open(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.error("Timed out waiting for WebSocket to open.")
            raise ConnectionError("WebSocket connection timeout.") from None

    async def _check_ws_open(self):
        while not self.ws or not self.ws.open:
            await asyncio.sleep(0.1)

    def _is_valid_message(self, data):
        if self.TOPIC_KEY not in data:
            return False

        return True

    async def _resubscribe_all(self):
        if not self.subscriptions:
            return

        await self._send(self.SUBSCRIBE_OPERATION, self.subscriptions)

        logger.info(f"Resubscribed to all topics: {self.subscriptions}")
