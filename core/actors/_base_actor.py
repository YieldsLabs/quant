import inspect
import uuid
from typing import Union, get_args, get_origin

from core.commands._base import Command
from core.events._base import Event
from core.interfaces.abstract_actor import AbstractActor, Ask, Message
from core.queries._base import Query
from core.tasks._base import Task
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher


class BaseActor(AbstractActor):
    def __init__(self):
        super().__init__()
        self._running = False
        self._mailbox = EventDispatcher()
        self._id = str(uuid.uuid4())
        self._EVENTS = self._discover_events()

    @property
    def id(self):
        return self._id

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
            raise RuntimeError(f"Start: {self.__class__.__name__} is already running")

        self._register_events()
        self.on_start()
        self._running = True

    def stop(self):
        if not self.running:
            raise RuntimeError(f"Stop: {self.__class__.__name__} is not started")

        self._unregister_events()
        self.on_stop()
        self._running = False

    async def tell(self, msg: Message, *args, **kwrgs):
        await self._mailbox.dispatch(msg, *args, **kwrgs)

    async def ask(self, msg: Ask, *args, **kwrgs):
        if isinstance(msg, Query):
            return await self._mailbox.query(msg, *args, **kwrgs)
        if isinstance(msg, Command):
            await self._mailbox.execute(msg, *args, **kwrgs)
        if isinstance(msg, Task):
            await self._mailbox.run(msg, *args, **kwrgs)

    def _register_events(self):
        for event in self._EVENTS:
            self._mailbox.register(event, self.on_receive, self.pre_receive)

    def _unregister_events(self):
        for event in self._EVENTS:
            self._mailbox.unregister(event, self.on_receive)

    def _discover_events(self):
        allowed_types = (Event, Query, Command, Task)
        sig = inspect.signature(self.on_receive)
        params = sig.parameters.values()

        if not params:
            raise RuntimeError(
                f"{self.on_receive.__name__} method must accept at least one parameter for event handling."
            )

        event_type = next(iter(params)).annotation

        events = (
            get_args(event_type) if get_origin(event_type) is Union else [event_type]
        )

        invalid_events = [
            event for event in events if not issubclass(event, allowed_types)
        ]

        if invalid_events:
            raise RuntimeError(
                f"Disallowed events: {', '.join(e.__name__ for e in invalid_events)}. "
                f"Must be subclasses of {allowed_types}."
            )

        return list(set(events))
