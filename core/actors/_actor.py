from core.commands.base import Command
from core.interfaces.abstract_actor import AbstractActor, Ask, Message
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.base import Query
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher


class Actor(AbstractActor):
    _EVENTS = []

    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._running = False
        self._mailbox = EventDispatcher()

    @property
    def id(self):
        return f"{self._symbol}_{self._timeframe}"

    @property
    def symbol(self):
        return self._symbol

    @property
    def timeframe(self):
        return self._timeframe

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
            self._mailbox.register(event, self.on_receive, self._pre_receive)

        self.on_start()
        self._running = True

    def stop(self):
        if not self.running:
            raise RuntimeError(f"Stop: {self.__class__.__name__} is not started")

        for event in self._EVENTS:
            self._mailbox.unregister(event, self.on_receive)

        self.on_stop()
        self._running = False

    async def tell(self, msg: Message, *args, **kwrgs):
        await self._mailbox.dispatch(msg, *args, **kwrgs)

    async def ask(self, msg: Ask, *args, **kwrgs):
        if isinstance(msg, Query):
            return await self._mailbox.query(msg, *args, **kwrgs)
        if isinstance(msg, Command):
            await self._mailbox.execute(msg, *args, **kwrgs)

    def _pre_receive(self, _msg: Message):
        return self.pre_receive(_msg)
