import logging
from typing import Optional, Tuple, Union

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
PerfKey = Tuple[Symbol, Timeframe, Strategy]


class PortfolioActor(BaseActor, EventHandlerMixin):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()

        self.config = config_service.get("portfolio")
        self.state = InMemory[PerfKey, Performance]()

        self.state.on_set.connect(self._notify_update)
        self.state.on_set.connect(self._log_update)

    async def on_receive(self, event: PortfolioEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(BacktestStarted, self._init_state)
        self.register_handler(TradeStarted, self._init_state)
        self.register_handler(PortfolioReset, self._reset_state)
        self.register_handler(PositionClosed, self._update_state)
        self.register_handler(GetPortfolioPerformance, self._get_performance)

    async def _init_state(self, event: Union[BacktestStarted, TradeStarted]):
        key = self._perf_key(event.symbol, event.timeframe, event.strategy)
        performance = await self._init_performance()

        await self.state.set(key, performance)

    async def _get_performance(
        self, event: GetPortfolioPerformance
    ) -> Optional[Performance]:
        key = self._perf_key(event.symbol, event.timeframe, event.strategy)
        performance = await self.state.get(key)

        if not performance:
            performance = await self._init_performance()
            await self.state.set(key, performance)

        return performance

    async def _reset_state(self, _event: PortfolioReset):
        await self.state.reset()

    async def _update_state(self, event: PositionClosed):
        position = event.position

        key = self._perf_key(
            position.signal.symbol,
            position.signal.timeframe,
            position.signal.strategy,
        )

        performance = await self.state.get(key)

        if performance and position.is_valid:
            next_performance = performance.next(position.pnl, position.fee)
            await self.state.set(key, next_performance)
        else:
            logger.warning(f"Invalid position: {position}")

    async def _init_performance(self):
        result = await self.ask(GetBalance())

        account_size = (
            self.config.get("account_size", 1000)
            if result.is_err()
            else result.unwrap()
        )
        risk_per_trade = self.config.get("risk_per_trade", 0.0001)

        return Performance(account_size, risk_per_trade)

    async def _notify_update(
        self, key: PerfKey, old_value: Performance, new_value: Performance
    ):
        symbol, timeframe, strategy = key

        await self.tell(
            PortfolioPerformanceUpdated(symbol, timeframe, strategy, new_value)
        )

    def _log_update(self, key: PerfKey, old_value: Performance, new_value: Performance):
        symbol, timeframe, strategy = key

        logger.info(
            f"{symbol}_{timeframe}{strategy}, "
            f"Trades={new_value.total_trades}, Hit={new_value.hit_ratio:.0%}, IR={new_value.information_ratio:.4f}, "
            f"CAGR={new_value.cagr:.2%}, Return={new_value.expected_return:.2%}, "
            f"Volatility={new_value.ann_volatility:.2%}, Sharpe={new_value.smart_sharpe_ratio:.4f}, "
            f"Sortino={new_value.sortino_ratio:.4f}, Omega={new_value.omega_ratio:.2f}, PnL={new_value.total_pnl:.4f}, Fee={new_value.total_fee:.4f}"
        )

    @staticmethod
    def _perf_key(symbol: Symbol, timeframe: Timeframe, strategy: Strategy) -> PerfKey:
        return symbol, timeframe, strategy
