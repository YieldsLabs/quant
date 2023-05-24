import asyncio
import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.portfolio import PortfolioPerformance, PortfolioPerformanceEvent


class CSVSync(AbstractEventManager):
    PERFORMANCE_CSV = "strategy_performance.csv"

    def __init__(self, save_interval: int = 10):
        super().__init__()
        self.perf_columns = [
            'timestamp',
            'strategy_id',
        ] + list(PortfolioPerformance.__annotations__.keys())

        self.perf_event = {}
        self.save_interval = save_interval
        self._save_task = None
        self.lock = asyncio.Lock()

        self.start_save_task()

    async def _periodic_save(self):
        while True:
            await asyncio.sleep(self.save_interval)
            self.save_to_csv()

    def start_save_task(self):
        self._save_task = asyncio.create_task(self._periodic_save())

    def save_to_csv(self):
        perf_df = pd.DataFrame(list(self.perf_event.values()), columns=self.perf_columns)
        perf_df.to_csv(self.PERFORMANCE_CSV, index=False)

    @register_handler(PortfolioPerformanceEvent)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceEvent):
        async with self.lock:
            event_dict = {
                'timestamp': int(event.meta.timestamp),
                'strategy_id': event.strategy_id
            }

            event_dict.update(event.performance.to_dict())
            self.perf_event[event.strategy_id] = event_dict
