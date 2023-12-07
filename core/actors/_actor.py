from core.commands.base import Command
from core.interfaces.abstract_actor import AbstractActor, Ask, Message
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.base import Query
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore


class Actor(AbstractActor):
    _EVENTS = []

    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._strategy = strategy
        self._running = False
        self._mailbox = EventDispatcher()
        self._store = EventStore()

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
    def running(self):
        return self._running

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def pre_receive(self, _msg: Message) -> bool:
        return True

    def on_receive(self, _msg: Message):
        pass

    def start(self):
        if self.running:
            raise RuntimeError(f"Start: {self.__class__.__name__} is running")

        for event in self._EVENTS:
            self._mailbox.register(event, self.on_receive, self.pre_receive)

        self.on_start()
        self._running = True

    def stop(self):
        if not self.running:
            raise RuntimeError(f"Stop: {self.__class__.__name__} is not started")

        for event in self._EVENTS:
            self._mailbox.unregister(event, self.on_receive)

        self.on_stop()
        self._running = False

    async def tell(self, msg: Message):
        await self._mailbox.dispatch(msg)
        self._store.append(msg)

    async def ask(self, msg: Ask):
        if isinstance(msg, Query):
            return await self._mailbox.query(msg)
        if isinstance(msg, Command):
            await self._mailbox.execute(msg)
