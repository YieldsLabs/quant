import asyncio

from core.events.base import Event

from .load_balancer import LoadBalancer
from .event_worker import EventWorker
from .event_handler import EventHandler

import heapq

class WorkerLoad:
    def __init__(self, worker):
        self.worker = worker
        self.current_load = 0

    def assign(self, event):
        self.current_load += 1

    def complete(self, event):
        self.current_load -= 1

    def __lt__(self, other):
        return self.current_load < other.current_load
    
    def __eq__(self, other: 'WorkerLoad') -> bool:
        return self.load == other.load


class WorkerPool:
    def __init__(self, num_workers: int, num_priority_group: int, event_handler: EventHandler, cancel_event: asyncio.Event):
        self.workers = [EventWorker(event_handler, cancel_event) for _ in range(num_workers)]
        self.load_balancer = LoadBalancer(num_priority_group)
        self.priority_to_worker_map = self._create_priority_map(num_workers, num_priority_group)

    def _create_priority_map(self, num_workers, num_priority_group):
        priority_map = {}

        for i in range(num_priority_group):
            priority_map[i] = i % num_workers
            
        return priority_map

    async def dispatch_to_worker(self, event: Event, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(event.meta.priority)
        worker_index = self.priority_to_worker_map[priority_group]
        await self.workers[worker_index].dispatch(event, *args, **kwargs)
        self.load_balancer.register_event(priority_group)

    async def wait(self) -> None:
        for worker in self.workers:
            await worker.wait()
