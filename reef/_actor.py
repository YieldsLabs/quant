import asyncio
import heapq
import logging
import time
from dataclasses import dataclass

from coral import DataSourceFactory
from core.actors import BaseActor
from core.events.market import NewMarketOrderReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.order_type import OrderType
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

logger = logging.getLogger(__name__)


@dataclass(order=True)
class PQOrder:
    timestamp: float
    order_id: str
    symbol: Symbol
    datasource: DataSourceType


class ReefActor(BaseActor):
    def __init__(
        self, datasource_factory: DataSourceFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self._lock = asyncio.Lock()
        self._orders = []
        self._datasource_factory = datasource_factory
        self._tasks = set()
        self.order_config = config_service.get("order")

    def on_start(self):
        monitor_task = asyncio.create_task(self._monitor_orders())
        monitor_task.add_done_callback(self._tasks.discard)
        self._tasks.add(monitor_task)

        worker_task = asyncio.create_task(self._process_order_queue())
        worker_task.add_done_callback(self._tasks.discard)
        self._tasks.add(worker_task)

    def on_stop(self):
        for task in list(self._tasks):
            task.cancel()

        self._tasks.clear()

    def pre_receive(self, event: NewMarketOrderReceived):
        return (
            isinstance(event, NewMarketOrderReceived)
            and event.order.type != OrderType.PAPER
        )

    async def on_receive(self, event: NewMarketOrderReceived):
        order = event.order

        async with self._lock:
            heapq.heappush(
                self._orders,
                PQOrder(time.time(), order.id, event.symbol, event.datasource),
            )
            logging.info(f"Order {order.id} {order.status} added to the queue.")

    async def _process_order_queue(self):
        while True:
            try:
                async with self._lock:
                    if not self._orders:
                        await asyncio.sleep(1)
                        continue

                    next_order = self._orders[0]
                    current_time = time.time()

                    if next_order.timestamp > current_time:
                        await asyncio.sleep(next_order.timestamp - current_time)
                        continue

                    prioritized_order = heapq.heappop(self._orders)

                await self._cancel_order(
                    prioritized_order.order_id,
                    prioritized_order.symbol,
                    prioritized_order.datasource,
                )

            except Exception as e:
                logging.error(f"Error processing order queue: {str(e)}")

    async def _cancel_order(
        self, order_id: str, symbol: Symbol, datasource: DataSourceType
    ):
        service = self._datasource_factory.create(datasource, ProtocolType.REST)

        await asyncio.to_thread(service.cancel_order, order_id, symbol)

        logging.info(f"Order {order_id} for symbol {symbol.name} canceled.")

    async def _monitor_orders(self):
        expiration_time = self.order_config.get("expiration_time", 10)
        monitor_interval = self.order_config.get("monitor_interval", 10)

        try:
            while True:
                await asyncio.sleep(monitor_interval)

                async with self._lock:
                    current_time = time.time()
                    expired_orders = [
                        order
                        for order in self._orders
                        if current_time - order.timestamp > expiration_time
                    ]

                    for expired_order in expired_orders:
                        await self._cancel_order(
                            expired_order.order_id,
                            expired_order.symbol,
                            expired_order.datasource,
                        )

                    self._orders = [
                        order for order in self._orders if order not in expired_orders
                    ]

        except asyncio.CancelledError:
            logging.info("Monitoring task canceled.")
        except Exception:
            logging.e

    async def _fetch_open_orders(self):
        services = [
            DataSourceType.BYBIT,
        ]

        for datasource in services:
            service = self._datasource_factory.create(datasource, ProtocolType.REST)
            orders = await asyncio.to_thread(service.fetch_all_open_orders)

            async with self._lock:
                for order_id, symbol in orders:
                    heapq.heappush(
                        self._orders, PQOrder(time.time(), order_id, symbol, datasource)
                    )
