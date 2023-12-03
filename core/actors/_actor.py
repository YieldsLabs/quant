import asyncio

from core.interfaces.abstract_actor import AbstractActor
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class Actor(AbstractActor):
    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy = strategy
        self._lock = asyncio.Lock()
        self._running = False

    @property
    def id(self):
        return f"{self._symbol}_{self._timeframe}{self._strategy}"

    @property
    def symbol(self):
        return self._symbol

    @property
    def timeframe(self):
        return self._timeframe

    @property
    def strategy(self):
        return self._strategy

    @property
    async def running(self):
        async with self._lock:
            return self._running

    async def start(self):
        if await self.running:
            raise RuntimeError(f"Start: {self.__class__.__name__} is running")
        self._running = True

    async def stop(self):
        if not await self.running:
            raise RuntimeError(f"Stop: {self.__class__.__name__} is not started")
        self._running = False
