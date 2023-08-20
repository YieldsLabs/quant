import asyncio
from functools import partial
import pandas as pd

from core.abstract_event_manager import AbstractEventManager
from core.event_decorators import register_handler
from core.events.portfolio import BasicPortfolioPerformance, AdvancedPortfolioPerformance, PortfolioPerformanceUpdated


class CSVSync(AbstractEventManager):
    SAVE_INTERVAL = 10
    PERFORMANCE_CSV = "strategy_performance.csv"

    def __init__(self):
        super().__init__()
        self.perf_columns = [
            'timestamp',
            'strategy',
        ] + list(BasicPortfolioPerformance.__annotations__.keys()) + list(AdvancedPortfolioPerformance.__annotations__.keys())

        self.perf_event = {}
        self._save_task = None
        self.lock = asyncio.Lock()

        self.start_save_task()

    @register_handler(PortfolioPerformanceUpdated)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceUpdated):
        async with self.lock:
            self.perf_event[event.strategy] = self._event_to_dict(event)

    async def _periodic_save(self):
        while True:
            await asyncio.sleep(self.SAVE_INTERVAL)
            await self.save_to_csv()

    def start_save_task(self):
        self._save_task = asyncio.create_task(self._periodic_save())

    async def save_to_csv(self):
        perf_df = pd.DataFrame.from_records(list(self.perf_event.values()), columns=self.perf_columns)
        await asyncio.to_thread(partial(perf_df.to_csv, self.PERFORMANCE_CSV, index=False))

    @staticmethod
    def _event_to_dict(event):
        event_dict = {'timestamp': int(event.meta.timestamp), 'strategy': event.strategy}
        event_dict.update(event.basic.to_dict())
        event_dict.update(event.advanced.to_dict())
        return event_dict
