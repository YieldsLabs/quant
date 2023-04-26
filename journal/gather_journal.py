import pandas as pd
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.portfolio import PortfolioPerformanceEvent


class GatherJournal(AbstractEventManager):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(columns=[
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
            'ulcer_index',
        ])

    @register_handler(PortfolioPerformanceEvent)
    async def _on_portfolio_performance(self, event: PortfolioPerformanceEvent):
        if event.performance.total_trades < 5:
            return

        event_dict = {
            'timestamp': int(event.meta.timestamp),
            'strategy_id': event.strategy_id,
        }

        event_dict.update(event.performance.to_dict())

        new_row = pd.DataFrame([event_dict])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        self.df.to_csv("strategy_performance.csv", index=False)
