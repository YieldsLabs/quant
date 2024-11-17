import asyncio
import logging
from typing import Any, AsyncIterable, Awaitable, Callable, Optional

from core.events._base import Event

STOP = object()

logger = logging.getLogger(__name__)


class DataCollector:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._producers = []
        self._consumers = []
        self._tasks = set()
        self._stop_event = asyncio.Event()

    async def start(self, msg: Event):
        for producer in self._producers:
            task = asyncio.create_task(self._run_producer(producer, msg))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        for consumer in self._consumers:
            task = asyncio.create_task(self._run_consumer(consumer))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

    async def stop(self):
        self._stop_event.set()
        self._queue.put_nowait(STOP)

        for task in self._tasks:
            task.cancel()

        tasks_to_cancel = [task for task in self._tasks if not task.done()]

        for task in tasks_to_cancel:
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.error(f"Error during task completion: {e}")

        self._tasks.clear()

    async def wait_for_completion(self):
        try:
            await asyncio.gather(*self._tasks)
        except Exception as e:
            logger.error(e)

    def add_producer(self, producer: Callable[[Optional[Event]], AsyncIterable[Any]]):
        self._producers.append(producer)

    def add_consumer(self, consumer: Callable[[Any], Awaitable[None]]):
        self._consumers.append(consumer)

    async def _run_producer(self, producer, msg):
        try:
            async for data in producer(msg):
                await self._queue.put(data)
        except asyncio.CancelledError:
            pass
        finally:
            await self._queue.put(STOP)

    async def _run_consumer(self, consumer):
        try:
            while not self._stop_event.is_set():
                data = await self._queue.get()

                try:
                    if data is STOP:
                        break

                    if data:
                        await consumer(data)
                except Exception as e:
                    logger.error(e)
                finally:
                    self._queue.task_done()
        except asyncio.CancelledError:
            pass
