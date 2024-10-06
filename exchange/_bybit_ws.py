import asyncio
import hashlib
import hmac
import json
import logging
import time

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
    AUTH_OPERATION = "auth"

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
    OP_KEY = "op"
    SUCCESS_KEY = "success"
    ARGS_KEY = "args"

    def __init__(self, wss: str, api_key: str, api_secret: str):
        super().__init__()
        self.wss = wss
        self.ws = None
        self.api_key = api_key
        self.api_secret = api_secret
        self._lock = asyncio.Lock()
        self.subscriptions = set()
        self._auth_event = asyncio.Event()
        self._message_queue = asyncio.Queue()
        self._tasks = set()
        self._semaphore = asyncio.Semaphore(1)

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
                await self._handle_reconnect()

                receive_task = asyncio.create_task(self._receive())
                self._tasks.add(receive_task)
                receive_task.add_done_callback(self._tasks.discard)
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
        if self._tasks:
            for task in self._tasks:
                task.cancel()

            await asyncio.gather(*self._tasks, return_exceptions=True)

            self._tasks.clear()

        if self.ws:
            await self.ws.close()
            await self.ws.wait_closed()
            self.ws = None

    async def auth(self):
        expires = int(time.time() * 10**3) + 3 * 10**3
        param_str = f"GET/realtime{expires}"
        sign = hmac.new(
            bytes(self.api_secret, "utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        await self._send(self.AUTH_OPERATION, [self.api_key, expires, sign])
        await self._auth_event.wait()

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=connect_exceptions,
    )
    async def _receive(self):
        await self._connect()

        async with self._semaphore:
            try:
                async for message in self.ws:
                    data = json.loads(message)

                    if self._is_auth_confirm_message(data):
                        self._auth_event.set()

                    if self._is_data_message(data):
                        await self._message_queue.put(data.get(self.DATA_KEY))
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Malformed message received: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while receiving message: {e}")
                raise ConnectionError("WebSocket connection error.") from None

    async def subscribe(self, topic: str):
        async with self._lock:
            await self._send(self.SUBSCRIBE_OPERATION, [topic])
            self.subscriptions.add(topic)

    async def unsubscribe(self, topic):
        async with self._lock:
            await self._send(self.UNSUBSCRIBE_OPERATION, [topic])

            if topic in self.subscriptions:
                self.subscriptions.remove(topic)

    async def get_message(self):
        message = await self._message_queue.get()
        self._message_queue.task_done()

        return message

    def kline_topic(self, timeframe: Timeframe, symbol: Symbol) -> str:
        return f"kline.{self.INTERVALS[timeframe]}.{symbol.name}"

    def order_book_topic(self, symbol: Symbol, depth: int):
        return f"orderbook.{depth}.{symbol.name}"

    def liquidation_topic(self, symbol: Symbol):
        return f"liquidation.{symbol.name}"

    def order_topic(self):
        return "order.linear"

    def position_topic(self):
        return "position.linear"

    async def _send(self, operation, args, timeout=5):
        if not self.ws or not self.ws.open:
            logger.error("WebSocket connection error.")
            return

        message = {
            self.OP_KEY: operation,
            self.ARGS_KEY: args,
        }

        try:
            await asyncio.wait_for(self.ws.send(json.dumps(message)), timeout=timeout)

            if operation != self.AUTH_OPERATION:
                logger.info(f"Subscribed {operation.capitalize()} to: {message}")
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

    def _is_data_message(self, data):
        return self.TOPIC_KEY in data

    def _is_auth_confirm_message(self, data):
        return (
            data.get(self.OP_KEY) == self.AUTH_OPERATION
            and data.get(self.SUCCESS_KEY) is True
        )

    async def _resubscribe_all(self):
        async with self._lock:
            if not self.subscriptions:
                return

            await self._send(self.SUBSCRIBE_OPERATION, list(self.subscriptions))

            logger.info(f"Resubscribed to all topics: {list(self.subscriptions)}")

    async def _handle_reconnect(self):
        if self._auth_event.is_set():
            await self.auth()

        await self._resubscribe_all()
