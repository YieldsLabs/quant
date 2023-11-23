import logging

from core.commands.account import UpdateAccountSize
from core.commands.portfolio import PortfolioReset
from core.event_decorators import command_handler, event_handler, query_handler
from core.events.account import PortfolioAccountUpdated
from core.events.backtest import BacktestStarted
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.size import PositionSizeType
from core.queries.portfolio import (
    GetFitness,
    GetPositionRisk,
    GetTopStrategy,
)

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

    @event_handler(BacktestStarted)
    async def handle_backtest_started(self, event: BacktestStarted):
        await self.state.reset(event.symbol, event.timeframe, event.strategy)

    @command_handler(PortfolioReset)
    async def portfolio_reset(self, _event: PortfolioReset):
        await self.state.reset_all()

    @event_handler(PositionClosed)
    async def handle_close_positon(self, event: PositionClosed):
        await self.state.next(event.position, self.account_size, self.risk_per_trade)

        signal = event.position.signal
        symbol = signal.symbol
        timeframe = signal.timeframe
        strategy = signal.strategy

        performance = await self.state.get(event.position)
        logger.info(
            f"Performance: strategy={symbol}_{timeframe}{strategy}, trades={performance.total_trades}, cagr={round(performance.cagr * 100, 2)}%, pnl={round(performance.total_pnl, 2)}"
        )

        await self.dispatch(
            PortfolioPerformanceUpdated(symbol, timeframe, strategy, performance)
        )

        await self.strategy.next(
            symbol,
            timeframe,
            strategy,
            [
                performance.calmar_ratio,
                performance.cvar,
                performance.ulcer_index,
                performance.max_drawdown,
                performance.annualized_return,
                performance.sterling_ratio,
                performance.sortino_ratio,
                performance.burke_ratio,
                performance.average_pnl,
            ],
        )

    @query_handler(GetTopStrategy)
    async def top_strategies(self, query: GetTopStrategy):
        strategies = await self.strategy.get_top(query.num)
        return strategies

    @query_handler(GetPositionRisk)
    async def equity(self, query: GetPositionRisk):
        symbol = query.signal.symbol
        timeframe = query.signal.timeframe
        strategy = query.signal.strategy

        equity = await self.state.get_equity(symbol, timeframe, strategy)

        if query.type == PositionSizeType.Fixed:
            return equity * self.risk_per_trade

        elif query.type == PositionSizeType.Kelly:
            kelly = await self.state.get_kelly(symbol, timeframe, strategy)
            return equity * kelly if kelly else self.risk_per_trade

        elif query.type == PositionSizeType.Optimalf:
            optimalf = await self.state.get_optimalf(symbol, timeframe, strategy)
            return equity * optimalf if optimalf else self.risk_per_trade

        else:
            return equity * self.risk_per_trade

    @query_handler(GetFitness)
    async def fitness(self, query: GetFitness):
        return await self.state.get_fitness(
            query.symbol, query.timeframe, query.strategy
        )
