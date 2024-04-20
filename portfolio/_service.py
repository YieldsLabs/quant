import asyncio
import logging
from collections import defaultdict

from core.commands.account import UpdateAccountSize
from core.commands.portfolio import PortfolioReset, StrategyReset
from core.event_decorators import command_handler, event_handler, query_handler
from core.events.account import PortfolioAccountUpdated
from core.events.backtest import BacktestStarted
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.events.trade import TradeStarted
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.size import PositionSizeType
from core.queries.portfolio import (
    GetFitness,
    GetPositionRisk,
    GetTopStrategy,
)

from ._portfolio import PortfolioStorage
from ._strategy import StrategyStorage

logger = logging.getLogger(__name__)


class Portfolio(AbstractEventManager):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.state = PortfolioStorage()
        self.strategy = StrategyStorage()
        self.config = config_service.get("portfolio")
        self.account_size = self.config["account_size"]

    @event_handler(BacktestStarted)
    async def handle_backtest_started(self, event: BacktestStarted):
        await self.state.reset(
            event.symbol,
            event.timeframe,
            event.strategy,
            self.account_size,
            self.config["risk_per_trade"],
        )

    @event_handler(TradeStarted)
    async def trade_started(self, event: TradeStarted):
        await asyncio.gather(
            *[
                self.state.reset(
                    event.symbol,
                    event.timeframe,
                    event.strategy,
                    self.account_size,
                    self.config["risk_per_trade"],
                ),
                self.strategy.reset(event.symbol, event.timeframe, event.strategy),
            ]
        )

    @event_handler(PositionClosed)
    async def handle_close_positon(self, event: PositionClosed):
        position = event.position
        signal = position.signal
        symbol = signal.symbol
        timeframe = signal.timeframe
        strategy = signal.strategy

        performance = await self.state.get(symbol, timeframe, strategy)

        if not performance or performance.updated_at < event.meta.timestamp:
            performance = await self.state.next(
                event.position, self.account_size, self.config["risk_per_trade"]
            )

        logger.info(
            f"Performance: strategy={symbol}_{timeframe}{strategy}, side={position.side}, "
            + f"trades={performance.total_trades}, hit_ratio={round(performance.hit_ratio * 100)}%, "
            + f"cagr={round(performance.cagr * 100, 2)}%, return={round(performance.expected_return * 100, 2)}%, volatility={round(performance.ann_volatility * 100, 2)}%, "
            + f"smart_sharpe={round(performance.smart_sharpe_ratio, 4)}, smart_sortino={round(performance.smart_sortino_ratio, 4)}, "
            + f"skew={round(performance.skew, 2)}, kurtosis={round(performance.kurtosis, 2)}, omega={round(performance.omega_ratio, 2)}, upi={round(performance.upi, 2)}, "
            + f"pnl={round(performance.total_pnl, 4)}, fee={round(performance.total_fee, 4)}"
        )

        await self.dispatch(
            PortfolioPerformanceUpdated(symbol, timeframe, strategy, performance)
        )

        performance_metrics = [
            performance.smart_sharpe_ratio,
            performance.smart_sortino_ratio,
            performance.calmar_ratio,
            performance.cvar,
            performance.ulcer_index,
            performance.sterling_ratio,
            performance.burke_ratio,
            performance.ann_volatility,
            performance.cpc_ratio,
            performance.rachev_ratio,
        ]

        await self.strategy.next(
            symbol,
            timeframe,
            strategy,
            performance_metrics,
        )

    @query_handler(GetTopStrategy)
    async def top_strategies(self, query: GetTopStrategy):
        strategies = await self.strategy.get_top(query.num * 3)

        if not query.positive_pnl:
            return strategies[: query.num]

        res = []
        strategy_by_symbol = defaultdict(list)

        for symbol, timeframe, strategy in strategies:
            performance = await self.state.get(symbol, timeframe, strategy)

            if (
                performance.cagr >= self.config["cagr_threshold"]
                and performance.smart_sharpe_ratio
                >= self.config["sharpe_ratio_threshold"]
            ) and performance.total_trades >= self.config["total_trades_threshold"]:
                strategy_by_symbol[symbol].append((symbol, timeframe, strategy))

        for strategy in strategy_by_symbol.values():
            res.extend(strategy[: query.num])

        return res

    @query_handler(GetPositionRisk)
    async def position_risk(self, query: GetPositionRisk):
        symbol = query.signal.symbol
        timeframe = query.signal.timeframe
        strategy = query.signal.strategy
        risk_per_trade = self.config["risk_per_trade"]

        equity = await self.state.get_equity(symbol, timeframe, strategy)

        if equity == 0:
            return risk_per_trade

        if query.type == PositionSizeType.Kelly:
            kelly = await self.state.get_kelly(symbol, timeframe, strategy)
            return equity * kelly if kelly > 0 else equity * risk_per_trade

        if query.type == PositionSizeType.Optimalf:
            optimalf = await self.state.get_optimalf(symbol, timeframe, strategy)
            return optimalf * equity if optimalf > 0 else equity * risk_per_trade

        return equity * risk_per_trade

    @query_handler(GetFitness)
    async def fitness(self, query: GetFitness):
        return await self.state.get_fitness(
            query.symbol, query.timeframe, query.strategy
        )

    @command_handler(UpdateAccountSize)
    async def update_account_size(self, command: UpdateAccountSize):
        self.account_size = command.amount

        await self.dispatch(PortfolioAccountUpdated(self.account_size))

    @command_handler(PortfolioReset)
    async def portfolio_reset(self, _event: PortfolioReset):
        await self.state.reset_all()

    @command_handler(StrategyReset)
    async def stategy_reset(self, _event: StrategyReset):
        await self.strategy.reset_all()
