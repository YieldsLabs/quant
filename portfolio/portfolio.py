from core.commands.account import UpdateAccountSize
from core.event_decorators import command_handler, event_handler, query_handler
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.queries.portfolio import GetTopStrategy, GetTotalPnL
from portfolio.portfolio_storage import PortfolioStorage
from portfolio.strategy_storage import StrategyStorage


class Portfolio(AbstractEventManager):
    def __init__(self, initial_account_size: float, risk_per_trade: int):
        super().__init__()
        self.state = PortfolioStorage()
        self.strategy = StrategyStorage()
        self.account_size = initial_account_size
        self.risk_per_trade = risk_per_trade

    @command_handler(UpdateAccountSize)
    async def update_account_size(self, command: UpdateAccountSize):
        self.account_size = command.amount

    @event_handler(PositionClosed)
    async def handle_close_positon(self, event: PositionClosed):
        await self.state.next(event.position, self.account_size, self.risk_per_trade)
        
        signal = event.position.signal
        timeframe = signal.timeframe
        symbol = signal.symbol
        strategy = signal.strategy

        performance = await self.state.get(event.position)
        
        await self.dispatcher.dispatch(
            PortfolioPerformanceUpdated(strategy, timeframe, symbol, performance))
        
        await self.strategy.next(strategy, symbol, [
            performance.max_drawdown,
            performance.calmar_ratio,
            performance.ulcer_index,
            performance.var,
            performance.sharpe_ratio,
            performance.profit_factor
        ])

    @query_handler(GetTopStrategy)
    async def top_strategies(self, query: GetTopStrategy):
         return await self.strategy.get_top(query.num)

    @query_handler(GetTotalPnL)
    async def total_pnl(self, query: GetTotalPnL):
        return await self.state.get_total_pnl(query.signal)