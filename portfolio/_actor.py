import logging
from typing import Union

from core.actors import BaseActor
from core.commands.account import UpdateAccountSize
from core.commands.portfolio import PortfolioReset
from core.events.backtest import BacktestStarted
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import PositionClosed
from core.events.trade import TradeStarted
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.queries.account import GetBalance
from core.queries.portfolio import GetPortfolioPerformance

from ._state import PortfolioState

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
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self.config = config_service.get("portfolio")
        self.account_size = self.config.get("account_size", 1000)
        self.state = PortfolioState()

    async def on_receive(self, event: PortfolioEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(BacktestStarted, self._init_state)
        self.register_handler(TradeStarted, self._init_state)
        self.register_handler(PortfolioReset, self._reset_state)
        self.register_handler(PositionClosed, self._update_state)
        self.register_handler(GetPortfolioPerformance, self._get_state)

    async def _init_state(self, event: Union[BacktestStarted, TradeStarted]):
        self.account_size = await self.ask(GetBalance())

        await self.state.init(
            event.symbol,
            event.timeframe,
            event.strategy,
            self.account_size,
            self.config.get("risk_per_trade", 0.0001),
        )

    async def _get_state(self, event: GetPortfolioPerformance):
        performance = await self.state.get(event.symbol, event.timeframe, event.strategy)
        return performance

    async def _reset_state(self, _event: PortfolioReset):
        await self.state.reset_all()

    async def _update_state(self, event: PositionClosed):
        self.account_size = await self.ask(GetBalance())

        position = event.position

        if not position.is_valid:
            logger.warn(f"Wrong position: {position}")
            return

        signal = position.signal
        symbol = signal.symbol
        timeframe = signal.timeframe
        strategy = signal.strategy

        performance = await self.state.get(symbol, timeframe, strategy)

        if not performance or performance.updated_at < event.meta.timestamp:
            performance = await self.state.next(
                event.position, self.account_size, self.config.get("risk_per_trade")
            )

        logger.info(
            f"Performance: strategy={symbol}_{timeframe}{strategy}, side={position.side}, "
            f"trades={performance.total_trades}, hit_ratio={performance.hit_ratio:.0%}, inf_ratio={performance.information_ratio:.4f}, "
            f"cagr={performance.cagr:.2%}, return={performance.expected_return:.2%}, ann_volatility={performance.ann_volatility:.2%}, "
            f"smart_sharpe={performance.smart_sharpe_ratio:.4f}, modified_sharpe={performance.modified_sharpe_ratio:.4f}, "
            f"sortino={performance.sortino_ratio:.4f}, omega={performance.omega_ratio:.2f}, upi={performance.upi:.2f}, "
            f"skew={performance.skew:.2f}, kurtosis={performance.kurtosis:.2f}, "
            f"pnl={performance.total_pnl:.4f}, fee={performance.total_fee:.4f}"
        )

        await self.tell(
            PortfolioPerformanceUpdated(symbol, timeframe, strategy, performance)
        )
