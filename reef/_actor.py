import asyncio
import time

from typing import Any, Dict, Tuple
from core.actors import BaseActor
from coral import DataSourceFactory
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.entity.order import Order
from core.models.order_type import OrderStatus
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol

class ReefActor(BaseActor):
    def __init__(self, datasource_factory: DataSourceFactory, config_service: AbstractConfig):
        super().__init__()
        self._lock = asyncio.Lock()
        self._orders: Dict[str, Tuple[float, Symbol]] = {}
        self._datasource_factory = datasource_factory
        self._tasks = set()
        self.order_service = datasource_factory.create(DataSourceType.BYBIT, ProtocolType.WS)
        
        order_config = config_service.get("order", {})
        self.expiration_time = order_config.get("expiration_time", 10)
        self.monitor_interval = order_config.get("monitor_interval", 10)

    def on_start(self):
        task = asyncio.create_task(self._monitor_orders)
        task.add_done_callback(self._tasks.discard)
        self._tasks.add(task)

    def on_stop(self):
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()

    async def on_receive(self, event: Any):
        match event.order.status:
            case OrderStatus.EXECUTED:
                await self._clear_order(event.order)
            case OrderStatus.PENDING:
                await self._append_order(event.order, event.symbol)

    async def _clear_order(self, order: Order):
        async with self._lock:
            self._orders.pop(order.id, None)

    async def _append_order(self, order: Order, symbol: Symbol):
        async with self._lock:
            self._orders[order.id] = (time.time(), symbol)

    async def _monitor_orders(self):
        while True:
            await asyncio.sleep(self.monitor_interval)

            async with self._lock:
                curr_time = time.time()
                
                expired_orders = [
                    (order_id, symbol)
                    for order_id, (timestamp, symbol) in self._orders.items()
                    if curr_time - timestamp > self.expiration_time
                ]

                for order_id, symbol in expired_orders:
                    self._orders.pop(order_id)
                    await self.order_service.cancel_order(order_id, symbol)
