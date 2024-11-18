import logging
from typing import Optional, Union

from core.actors import BaseActor
from core.actors.state import InMemory
from core.commands.account import UpdateAccountSize
from core.commands.portfolio import PortfolioReset
from core.events.backtest import BacktestStarted
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.events.trade import TradeStarted
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.entity.portfolio import Performance
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.account import GetBalance
from core.queries.portfolio import GetPortfolioPerformance

PortfolioEvent = Union[
    BacktestStarted,
    TradeStarted,
    UpdateAccountSize,
    PortfolioReset,
    PositionClosed,
    GetPortfolioPerformance,
]

logger = logging.getLogger(__name__)


class PortfolioActor(BaseActor, EventHandlerMixin):
    ACCOUNT_SIZE_KEY = "__account_size__"

    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

        self.config = config_service.get("portfolio")
        self.state = InMemory[str, Union[Performance, float]]()

    async def on_receive(self, event: PortfolioEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(BacktestStarted, self._init_state)
        self.register_handler(TradeStarted, self._init_state)
        self.register_handler(PortfolioReset, self._reset_state)
        self.register_handler(PositionClosed, self._update_state)
        self.register_handler(GetPortfolioPerformance, self._get_performance)

    async def _init_state(self, event: Union[BacktestStarted, TradeStarted]):
        account_size = await self._update_account_size()
        risk_per_trade = self.config.get("risk_per_trade", 0.0001)
        key = self._performance_key(event.symbol, event.timeframe, event.strategy)

        await self.state.set(key, Performance(account_size, risk_per_trade))

    async def _get_performance(
        self, event: GetPortfolioPerformance
    ) -> Optional[Performance]:
        key = self._performance_key(event.symbol, event.timeframe, event.strategy)
        performance = await self.state.get(key)

        if not performance:
            account_size = await self.state.get(self.ACCOUNT_SIZE_KEY)
            risk_per_trade = self.config.get("risk_per_trade", 0.0001)
            performance = Performance(account_size, risk_per_trade)

            await self.state.set(key, performance)

        return performance

    async def _reset_state(self, _event: PortfolioReset):
        await self.state.reset()
        await self._update_account_size()

    async def _update_state(self, event: PositionClosed):
        position = event.position

        key = self._performance_key(
            position.signal.symbol,
            position.signal.timeframe,
            position.signal.strategy,
        )

        performance = await self.state.get(key)

        if performance and position.is_valid:
            next_performance = performance.next(position.pnl, position.fee)

            await self.state.set(key, next_performance)

            logger.info(
                f"{position.signal.symbol}_{position.signal.timeframe}:{position.side}{position.signal.strategy}: "
                f"Trades={performance.total_trades}, Hit={performance.hit_ratio:.0%}, IR={performance.information_ratio:.4f}, "
                f"CAGR={performance.cagr:.2%}, Return={performance.expected_return:.2%}, "
                f"Volatility={performance.ann_volatility:.2%}, Sharpe={performance.smart_sharpe_ratio:.4f}, "
                f"Sortino={performance.sortino_ratio:.4f}, Omega={performance.omega_ratio:.2f}, PnL={performance.total_pnl:.4f}, Fee={performance.total_fee:.4f}"
            )

            await self.tell(
                PortfolioPerformanceUpdated(
                    position.signal.symbol,
                    position.signal.timeframe,
                    position.signal.strategy,
                    next_performance,
                )
            )
        else:
            logger.warning(f"Invalid position: {position}")

    async def _update_account_size(self) -> float:
        account_size = await self.ask(GetBalance())

        await self.state.set(self.ACCOUNT_SIZE_KEY, account_size)

        return account_size

    @staticmethod
    def _performance_key(
        symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ) -> str:
        return f"{symbol}_{timeframe}_{strategy}"
