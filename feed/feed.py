import asyncio
import json
import logging

import websockets
from websockets.exceptions import ConnectionClosedError

from core.commands.feed import FeedRun
from core.event_decorators import command_handler
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_secret_service import AbstractSecretService
from core.interfaces.abstract_ws import AbstractWS
from core.models.exchange import ExchangeType
from core.models.ohlcv import OHLCV
from core.models.timeframe import Timeframe
from core.queries.broker import GetSymbol
from infrastructure.retry import retry

logger = logging.getLogger(__name__)


class Feed(AbstractWS):
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

    def __init__(self, secret: AbstractSecretService):
        super().__init__()
        self.ws = None
        self.secret = secret
        self.strategies = []

    async def connect_to_websocket(self, interval=5):
        await self.close()
        self.ws = await websockets.connect(self.secret.get_wss(ExchangeType.BYBIT.name))
        await asyncio.sleep(interval)

        if not self.ws.open:
            raise RuntimeError("Reconnect WS")

    async def process_message(self, message):
        message_data = json.loads(message)

        if self.TOPIC_KEY in message_data:
            ohlcv = message_data[self.DATA_KEY][0]
            topic = message_data[self.TOPIC_KEY].split(".")
            symbol, interval = topic[2], topic[1]

            if interval not in self.TIMEFRAMES:
                logger.error(f"Unknown interval: {interval}")
                return None

            ohlcv_event = await self.parse_candle_message(symbol, interval, ohlcv)

            if ohlcv[self.CONFIRM_KEY]:
                logger.info(f"Tick: {symbol}:{interval}:{ohlcv_event}")

            await self.dispatch(ohlcv_event)

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)

            if not self.ws:
                continue

            if not self.ws.open:
                continue

            pong = await self.ws.ping()
            await pong

    async def process_messages(self):
        async for message in self.ws:
            await self.process_message(message)

    @retry(
        max_retries=8,
        initial_retry_delay=1,
        handled_exceptions=(ConnectionError, RuntimeError, ConnectionClosedError),
    )
    async def run(self, ping_interval=15):
        try:
            await self.connect_to_websocket()

            ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))
            message_processing_task = asyncio.create_task(self.process_messages())

            if self.strategies:
                await self._subscribe()

            done, pending = await asyncio.wait(
                [ping_task, message_processing_task],
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

    async def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV.from_dict(data)
        symbol = await self.query(GetSymbol(symbol))
        return NewMarketDataReceived(
            symbol, self.TIMEFRAMES[interval], ohlcv, data[self.CONFIRM_KEY]
        )

    @command_handler(FeedRun)
    async def subscribe(self, command: FeedRun):
        if not self.ws or not self.ws.open:
            logger.error("WebSocket is not connected or open.")
            return

        self.strategies.append((command.symbol, command.timeframe, command.strategy))
        await self._subscribe()

    async def _subscribe(self):
        symbols_timeframes = [
            (strategy[0], strategy[1]) for strategy in self.strategies
        ]

        channels = [
            f"{self.KLINE_CHANNEL}.{self.INTERVALS[timeframe]}.{symbol}"
            for symbol, timeframe in symbols_timeframes
        ]

        subscribe_message = json.dumps(
            {"op": self.SUBSCRIBE_OPERATION, "args": channels}
        )

        await self.ws.send(subscribe_message)