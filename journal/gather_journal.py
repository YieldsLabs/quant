import asyncio
import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.portfolio import PortfolioPerformanceEvent


class GatherJournal(AbstractEventManager):
    def __init__(self, save_interval: int = 30):
        super().__init__()
        self.columns = [
            'timestamp',
            'strategy_id',
            'total_trades',
            'successful_trades',
            'win_rate',
            'risk_of_ruin',
            'rate_of_return',
            'annualized_return',
            'annualized_volatility',
            'total_pnl',
            'average_pnl',
            'sharpe_ratio',
            'sortino_ratio',
            'lake_ratio',
            'burke_ratio',
            'rachev_ratio',
            'tail_ratio',
            'omega_ratio',
            'sterling_ratio',
            'kappa_three_ratio',
            'profit_factor',
            'max_consecutive_wins',
            'max_consecutive_losses',
            'max_drawdown',
            'recovery_factor',
            'skewness',
            'kurtosis',
            'calmar_ratio',
            'var',
            'cvar',
            'ulcer_index'
        ]

        self.event = {}
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
        df = pd.DataFrame(list(self.event.values()), columns=self.columns)
        df.to_csv("strategy_performance.csv", index=False)

    @register_handler(PortfolioPerformanceEvent)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceEvent):
        async with self.lock:
            event_dict = {'timestamp': int(event.meta.timestamp), 'strategy_id': event.strategy_id}

            event_dict.update(event.performance.to_dict())
            self.event[event.strategy_id] = event_dict
