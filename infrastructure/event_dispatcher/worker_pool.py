import asyncio
from typing import List

import numpy as np

from core.events._base import Event

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
        alpha: float = 0.7,
        beta: float = 0.3
    ):
        self.workers = []
        self.load_balancer = LoadBalancer(num_piority_groups)
        self.dedup = EventDedup()
        self.event_handler = event_handler
        self.cancel_event = cancel_event
        self._num_priority_groups = num_piority_groups
        self._initialize_workers(num_workers)
        self.alpha = alpha
        self.beta = beta

    async def dispatch_to_worker(self, event: Event, *args, **kwargs) -> None:
        priority_group = self.load_balancer.determine_priority_group(
            event.meta.priority
        )

        if await self.dedup.acquire(event):
            group_workers = self._distribute_workers(priority_group)

            worker = self._choose_worker(group_workers)

            await worker.dispatch(event, *args, **kwargs)

        self.load_balancer.register_event(priority_group)

    async def wait(self) -> None:
        await asyncio.gather(*(worker.wait() for worker in self.workers))

    def _initialize_workers(self, num_workers):
        self.workers = [
            EventWorker(self.event_handler, self.cancel_event)
            for _ in range(num_workers * self._num_priority_groups)
        ]

        asyncio.gather(*(worker.run() for worker in self.workers))

    def _distribute_workers(self, priority_group: int) -> List[EventWorker]:
        workers_per_group = len(self.workers) // self._num_priority_groups
        group_start = priority_group * workers_per_group
        group_end = group_start + workers_per_group

        return self.workers[group_start:group_end]

    def _choose_worker(self, group_workers: List[EventWorker]) -> EventWorker:
        scores = np.array([worker.score for worker in group_workers])
        queue_sizes, median_times = scores[:, 0], scores[:, 1]

        norm_queue_sizes = (queue_sizes - queue_sizes.min() + 1) / (
            queue_sizes.max() - queue_sizes.min() + 1
        )
        norm_median_times = (median_times - median_times.min() + 1) / (
            median_times.max() - median_times.min() + 1
        )

        combined_scores = self.alpha * norm_queue_sizes + self.beta * norm_median_times

        weights = 1 / (combined_scores + 1e-6)
        total_weight = sum(weights)

        choice_point = np.random.uniform(0, total_weight)
        cum_weights = np.cumsum(weights)
        worker_index = np.searchsorted(cum_weights, choice_point)

        return group_workers[worker_index]
