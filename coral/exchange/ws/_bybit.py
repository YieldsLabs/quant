import asyncio
import hashlib
import hmac
import json
import logging
import time
import uuid

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosedError

from core.interfaces.abstract_exchange import AbstractWSExchange
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

logger = logging.getLogger(__name__)

connect_exceptions = (ConnectionError, ConnectionClosedError, asyncio.TimeoutError)

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"


class BybitWS(AbstractWSExchange):
    SUBSCRIBE_OPERATION = "subscribe"
    UNSUBSCRIBE_OPERATION = "unsubscribe"
    AUTH_OPERATION = "auth"
    PING_OPERATION = "ping"
    PONG_OPERATION = "pong"

    PING_INTERVAL = 20
    PING_TIMEOUT = 5
    PONG_TIMEOUT = 18
    AUTH_TIMEOUT = 10
    SEND_TIMEOUT = 5

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
    REQ_KEY = "req_id"
    RETR_MSG = "ret_msg"

    def __init__(self, wss: str, api_key: str, api_secret: str):
        super().__init__()
        self.wss = wss
        self.ws = None
        self.api_key = api_key
        self.api_secret = api_secret
        self._lock = asyncio.Lock()
        self._subscriptions = {}
        self._auth_event = asyncio.Event()
        self._topic_queues = {}
        self._tasks = set()
        self._semaphore = asyncio.Semaphore(1)
        self._receive_task = None
        self._ping_rid = str(uuid.uuid4())

    async def _connect(self):
        if not self.ws:
            try:
                self.ws = await connect(
                    self.wss,
                    open_timeout=5,
                    ping_interval=self.PING_INTERVAL,
                    ping_timeout=self.PONG_TIMEOUT,
                    close_timeout=10,
                    user_agent_header=user_agent,
                    max_queue=8,
                )

                await self._wait_for_ws(timeout=5)
                await self.ping()
                logger.info("WebSocket connection established.")
                self._start_tasks()
                await self._handle_reconnect()
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
            try:
                await self.ws.close()
            except Exception as e:
                logger.error(f"Failed to close WebSocket properly: {e}")
            finally:
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
        await asyncio.wait_for(self._auth_event.wait(), timeout=self.AUTH_TIMEOUT)

    async def ping(self):
        await asyncio.wait_for(
            self.ws.send(
                json.dumps(
                    {
                        self.OP_KEY: self.PING_OPERATION,
                        self.REQ_KEY: self._ping_rid,
                    }
                )
            ),
            timeout=self.PING_TIMEOUT,
        )

    def _start_tasks(self):
        if not self._receive_task or self._receive_task.done():
            self._receive_task = asyncio.create_task(self._receive())
            self._tasks.add(self._receive_task)
            self._receive_task.add_done_callback(self._tasks.discard)

    @retry(
        max_retries=13,
        initial_retry_delay=1,
        handled_exceptions=connect_exceptions,
    )
    async def _receive(self):
        async with self._semaphore:
            try:
                async for message in self.ws:
                    data = await self._parse_message(message)

                    if not data:
                        continue

                    await self._route_message(data)

            except Exception as e:
                logger.error(f"Unexpected error while receiving message: {e}")
                await self.connect()
                raise ConnectionError("WebSocket connection error.") from None

    async def subscribe(self, topic: str):
        await self._send(self.SUBSCRIBE_OPERATION, [topic])

        if topic not in self._topic_queues:
            self._topic_queues[topic] = asyncio.Queue()

    async def unsubscribe(self, topic: str):
        await self._send(self.UNSUBSCRIBE_OPERATION, [topic])
        self._topic_queues.pop(topic, None)

    async def get_message(self, topic: str):
        if topic not in self._topic_queues:
            logger.error(f"No queue available for topic: {topic}")
            return None

        message = await self._topic_queues[topic].get()
        self._topic_queues[topic].task_done()
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

    async def _send(self, operation, topics):
        if not self.ws:
            logger.error("WebSocket connection error.")
            return

        req_id = str(uuid.uuid4())

        message = {
            self.OP_KEY: operation,
            self.ARGS_KEY: topics,
            self.REQ_KEY: req_id,
        }

        try:
            await asyncio.wait_for(
                self.ws.send(json.dumps(message)), timeout=self.SEND_TIMEOUT
            )

            if operation == self.SUBSCRIBE_OPERATION:
                self._subscriptions[req_id] = message

            if operation == self.UNSUBSCRIBE_OPERATION:
                unsub_ids = {
                    req_id
                    for req_id, message in self._subscriptions.items()
                    if any(topic in message.get(self.ARGS_KEY, []) for topic in topics)
                }

                for rid in unsub_ids:
                    self._subscriptions.pop(rid, None)

            if operation != self.AUTH_OPERATION:
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

    async def _add_data(self, data):
        topic = data.get(self.TOPIC_KEY)
        message = data.get(self.DATA_KEY)

        if topic is None or message is None:
            logger.warning(f"Received data with missing topic or data: {data}")
            return

        queue = self._topic_queues.get(topic)

        if queue:
            await queue.put(message)
        else:
            queue = asyncio.Queue()
            await queue.put(message)
            
        self._topic_queues[topic] = queue

    async def _check_ws_open(self):
        while not self.ws:
            await asyncio.sleep(0.1)

    def _is_data_message(self, data):
        return self.TOPIC_KEY in data

    def _is_subs_confirm_message(self, data):
        return data.get(self.OP_KEY) == self.SUBSCRIBE_OPERATION

    def _is_pong_message(self, data):
        return (
            data.get(self.RETR_MSG) == self.PONG_OPERATION
            or data.get(self.OP_KEY) == self.PONG_OPERATION
        )

    def _is_auth_confirm_message(self, data):
        return (
            data.get(self.OP_KEY) == self.AUTH_OPERATION
            and data.get(self.SUCCESS_KEY) is True
        )

    async def _resubscribe(self, data):
        if not self._subscriptions:
            return

        req_id = data.get(self.REQ_KEY)

        if req_id is None:
            logger.error("Missing request ID in the response during resubscription.")
            return

        message = self._subscriptions.get(req_id)

        if not message:
            logger.error(f"Subscription message for req_id {req_id} not found.")
            return

        success = data.get(self.SUCCESS_KEY)

        if not success:
            await asyncio.wait_for(
                self.ws.send(json.dumps(message)), timeout=self.SEND_TIMEOUT
            )

            logger.info(f"Resubscribed to {message.get(self.ARGS_KEY)}")

    async def _resubscribe_all(self):
        if not self._subscriptions:
            return

        tasks = [
            asyncio.wait_for(
                self.ws.send(json.dumps(message)), timeout=self.SEND_TIMEOUT
            )
            for message in self._subscriptions.values()
        ]

        await asyncio.gather(*tasks)

        logger.info("Resubscribed to all topics")

    async def _handle_reconnect(self):
        if not self.ws:
            logger.error("WebSocket connection error.")
            return

        if self._auth_event.is_set():
            await self.auth()

        await self._resubscribe_all()

    async def _parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode message: {message}. Error: {e}")
            return None

    async def _route_message(self, data):
        if self._is_pong_message(data):
            await self.ping()
        elif self._is_auth_confirm_message(data):
            self._auth_event.set()
        elif self._is_subs_confirm_message(data):
            print(data)
            await self._resubscribe(data)
        elif self._is_data_message(data):
            await self._add_data(data)
