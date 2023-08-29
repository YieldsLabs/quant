import numpy as np

from core.events.portfolio import BasicPortfolioPerformance


class PortfolioBasicPerformance:
    def __init__(self, periods_per_year: int = 252):
        self.periods_per_year = periods_per_year

    def next(self, positions, initial_account_size, risk_per_trade) -> BasicPortfolioPerformance:
        total_trades = len(positions)

        if total_trades == 0:
            return BasicPortfolioPerformance(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        pnl = np.array([position.pnl for position in positions if len(position.orders) > 0])
        
        # pnl_positive = pnl > 0
        # successful_trades = pnl_positive.sum()
        # win_rate = successful_trades / total_trades
        # total_pnl = pnl.sum()
        # average_pnl = pnl.mean()
        
        annualized_return = self._annualized_return(rate_of_return, total_trades, self.periods_per_year)
        annualized_volatility = self._annualized_volatility(pnl, initial_account_size, self.periods_per_year)
        
        max_drawdown = self._max_drawdown(pnl, initial_account_size)
        max_consecutive_wins = self._max_streak(pnl_positive, True)
        max_consecutive_losses = self._max_streak(pnl_positive, False)
        
        rate_of_return = self._rate_of_return(total_pnl, initial_account_size)
        risk_of_ruin = self._risk_of_ruin(win_rate, initial_account_size, risk_per_trade)
        recovery_factor = self._recovery_factor(pnl, max_drawdown)
        calmar_ratio = self._calmar_ratio(rate_of_return, max_drawdown)

        return BasicPortfolioPerformance(
            max_consecutive_wins=max_consecutive_wins,
            max_consecutive_losses=max_consecutive_losses,
            risk_of_ruin=risk_of_ruin,
            rate_of_return=rate_of_return,
            annualized_return=annualized_return,
            annualized_volatility=annualized_volatility,
            max_drawdown=max_drawdown,
            recovery_factor=recovery_factor,
            calmar_ratio=calmar_ratio
        )
    
    @staticmethod
    def _risk_of_ruin(win_rate: float, initial_account_size: float, risk_per_trade: float) -> float:
        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        risk_of_ruin = ((1 - (risk_per_trade * (1 - loss_rate / win_rate))) ** initial_account_size) * 100

        return risk_of_ruin
    
    @staticmethod
    def _rate_of_return(total_pnl, initial_account_size) -> float:
        account_size = initial_account_size + total_pnl

        return (account_size / initial_account_size) - 1
    
    @staticmethod
    def _annualized_return(rate_of_return: float, total_trades: int, periods_per_year: int) -> float:
        if rate_of_return < 0 and periods_per_year % total_trades != 0:
            return 0

        holding_period_return = 1 + rate_of_return
        annualized_return = holding_period_return ** (periods_per_year / total_trades) - 1

        return annualized_return
    
    @staticmethod
    def _annualized_volatility(pnl, initial_account_size, periods_per_year: int) -> float:
        total_periods = len(pnl)

        if total_periods < 2:
            return 0

        daily_returns = pnl / initial_account_size
        volatility = np.std(daily_returns, ddof=1)
        annualized_volatility = volatility * np.sqrt(periods_per_year)

        return annualized_volatility
    
    @staticmethod
    def _max_drawdown(pnl, initial_account_size) -> float:
        account_size = initial_account_size
        peak = account_size
        max_drawdown = 0

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown
    
    @staticmethod
    def _max_streak(pnl_positive, winning: bool) -> int:
        streak = max_streak = 0

        for pnl_value in pnl_positive:
            if pnl_value == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak
    
    @staticmethod
    def _recovery_factor(pnl, max_drawdown) -> float:
        total_profit = pnl[pnl > 0].sum()

        return total_profit / max_drawdown if max_drawdown != 0 else 0
    
    @staticmethod
    def _calmar_ratio(rate_of_return: float, max_drawdown: float) -> float:
        if max_drawdown == 0:
            return 0

        calmar_ratio = rate_of_return / abs(max_drawdown)

        return calmar_ratio
