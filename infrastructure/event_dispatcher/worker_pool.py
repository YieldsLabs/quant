import asyncio

from core.events.base import Event

from .event_dedup import EventDedup
from .event_handler import EventHandler
from .event_worker import EventWorker
from .load_balancer import LoadBalancer


class WorkerPool:
    def __init__(
        self,
        num_workers: int,
        num_piority_groups: int,
        event_handler: EventHandler,
        cancel_event: asyncio.Event,
    ):
        self.workers = []
        self.load_balancer = LoadBalancer(num_piority_groups)
        self.dedup = EventDedup()
        self.event_handler = event_handler
        self.cancel_event = cancel_event
        self._initialize_workers(num_workers)

    def _initialize_workers(self, num_workers):
        self.workers = [
            EventWorker(self.event_handler, self.cancel_event, self.dedup)
            for _ in range(num_workers)
        ]

    async def dispatch_to_worker(self, event: Event, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(
            event.meta.priority
        )
        worker = self.workers[priority_group % len(self.workers)]

        await worker.dispatch(event, *args, **kwargs)
        self.load_balancer.register_event(priority_group)

    async def wait(self) -> None:
        await asyncio.gather(*(worker.wait() for worker in self.workers))
