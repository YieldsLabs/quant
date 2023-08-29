import numpy as np


class Performance:
    def __init__(self, account_size: float, risk_per_trade: float, periods_per_year: int = 252):
        self.pnl = np.array([])
        self.account_size = account_size
        self.risk_per_trade = risk_per_trade
        self.periods_per_year = periods_per_year
    
    def next(self, pnl):
        self.pnl = np.append(self.pnl, pnl)

    @property
    def total_pnl(self):
        return self.pnl.sum()


    