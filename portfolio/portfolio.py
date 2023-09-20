import logging

from core.commands.account import UpdateAccountSize
from core.event_decorators import command_handler, event_handler, query_handler
from core.events.account import PortfolioAccountUpdated
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.queries.portfolio import GetFitness, GetTopStrategy, GetTotalPnL

from .portfolio_storage import PortfolioStorage
from .strategy_storage import StrategyStorage


logger = logging.getLogger(__name__)


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

        await self.dispatch(PortfolioAccountUpdated(self.account_size))

    @event_handler(PositionClosed)
    async def handle_close_positon(self, event: PositionClosed):
        await self.state.next(event.position, self.account_size, self.risk_per_trade)
        
        signal = event.position.signal
        symbol = signal.symbol
        timeframe = signal.timeframe
        strategy = signal.strategy

        performance = await self.state.get(event.position)

        logger.info(f"Performance: strategy={symbol}_{timeframe}{strategy}, trades={performance.total_trades}, pnl={performance.total_pnl}")
        
        await self.dispatch(
            PortfolioPerformanceUpdated(symbol, timeframe, strategy, performance))
        
        await self.strategy.next(symbol, timeframe, strategy, [
            performance.calmar_ratio,
            performance.ulcer_index,
            performance.var,
            performance.sharpe_ratio,
            performance.profit_factor,
            performance.max_drawdown
        ])

    @query_handler(GetTopStrategy)
    async def top_strategies(self, query: GetTopStrategy):
         return await self.strategy.get_top(query.num)

    @query_handler(GetTotalPnL)
    async def total_pnl(self, query: GetTotalPnL):
        return await self.state.get_total_pnl(query.signal)
    
    @query_handler(GetFitness)
    async def fitness(self, query: GetFitness):
        return await self.strategy.get_fitness(query.symbol, query.timeframe, query.strategy)