from typing import Type, Union

from core.event_decorators import register_handler
from core.events.ohlcv import NewMarketDataReceived
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import ActivePositionOpened, PositionClosed, OrderFilled, LongPositionOpened, ClosePositionPrepared, ShortPositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from core.models.position import Position, PositionSide
from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_portfolio_manager import AbstractPortfolioManager

from .position_state_machine import PositionStateMachine
from .position_sizer import PositionSizer
from .position_storage import PositionStorage


class PortfolioManager(AbstractPortfolioManager):
    def __init__(self, datasource: Type[AbstractDatasource], initial_account_size: int = 1000, leverage: int = 1, risk_reward_ratio: int = 1.5, risk_per_trade: float = 0.001):
        super().__init__()
        self.datasource = datasource
        self.initial_account_size = initial_account_size
        self.leverage = leverage
        self.risk_reward_ratio = risk_reward_ratio
        self.risk_per_trade = risk_per_trade

        self.position_storage = PositionStorage()
        self.sm = PositionStateMachine(self)

    async def initialize_account(self):
        self.initial_account_size = await self.datasource.account_size()

    async def get_top_strategies(self, n):
        return await self.position_storage.get_top_strategies(self.initial_account_size, n)

    @register_handler(NewMarketDataReceived)
    async def _on_market(self, event: NewMarketDataReceived):
        await self.sm.process_event(event)

    @register_handler(GoLongSignalReceived)
    async def _on_go_long(self, event: GoLongSignalReceived):
        await self.sm.process_event(event)

    @register_handler(GoShortSignalReceived)
    async def _on_go_short(self, event: GoShortSignalReceived):
        await self.sm.process_event(event)

    @register_handler(ExitLongSignalReceived)
    async def _on_exit_long(self, event: ExitLongSignalReceived):
        await self.sm.process_event(event)

    @register_handler(ExitShortSignalReceived)
    async def _on_exit_short(self, event: ExitShortSignalReceived):
        await self.sm.process_event(event)

    @register_handler(RiskThresholdBreached)
    async def _on_exit_risk(self, event: RiskThresholdBreached):
        await self.sm.process_event(event)

    @register_handler(OrderFilled)
    async def _on_order_filled(self, event: OrderFilled):
        await self.sm.process_event(event)

    @register_handler(PositionClosed)
    async def _on_closed_position(self, event: PositionClosed):
        await self.sm.process_event(event)

    async def handle_open_position(self, event: Union[GoLongSignalReceived, GoShortSignalReceived]) -> bool:
        active_position = await self.position_storage.get_active_position(event.symbol)

        if active_position is not None:
            return False

        position = await self.create_position(event)

        await self.position_storage.add_active_position(event.symbol, position)

        open_position_event = self.create_open_position_event(position)

        await self.dispatcher.dispatch(open_position_event)

        return True

    async def handle_order_filled(self, event: OrderFilled) -> bool:
        active_position = await self.position_storage.get_active_position(event.symbol)

        if active_position is None:
            return False

        await self.position_storage.add_order(event.symbol, event.order)

        return True

    async def handle_closed_position(self, event: PositionClosed) -> bool:
        active_position = await self.position_storage.get_active_position(event.symbol)

        if active_position is None:
            return False

        strategy = active_position.strategy

        await self.position_storage.close_position(event.symbol, event.exit_price)
        await self.update_position_performance(strategy)

        return True

    async def handle_market(self, event: NewMarketDataReceived) -> bool:
        active_position = await self.position_storage.get_active_position(event.symbol)

        if active_position is None:
            return False

        await self.dispatcher.dispatch(
            ActivePositionOpened(
                symbol=active_position.symbol,
                timeframe=active_position.timeframe,
                side=active_position.side,
                size=active_position.size,
                entry=active_position.entry_price,
                stop_loss=active_position.stop_loss_price,
                risk_reward_ratio=active_position.risk_reward_ratio,
                strategy=active_position.strategy,
                risk_per_trade=self.risk_per_trade,
                ohlcv=event.ohlcv
            )
        )

        return True

    async def handle_exit(self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached]) -> bool:
        active_position = await self.position_storage.get_active_position(event.symbol)

        if active_position is None or (event.strategy != active_position.strategy) or not self.can_close_position(active_position.side, active_position.entry_price, event):
            return False

        await self.dispatcher.dispatch(
            ClosePositionPrepared(
                symbol=event.symbol,
                timeframe=event.timeframe,
                exit_price=event.exit
            )
        )

        return True

    async def create_position(self, event: Union[GoLongSignalReceived, GoShortSignalReceived]) -> Position:
        trading_fee, min_position_size, position_precision, price_precision = await self.datasource.fee_and_precisions(event.symbol)

        stop_loss_price = round(event.stop_loss, price_precision) if event.stop_loss else None
        entry_price = round(event.entry, price_precision)

        account_size = self.initial_account_size + await self.position_storage.total_pnl()

        size = PositionSizer.calculate_position_size(
            account_size,
            entry_price,
            trading_fee,
            min_position_size,
            position_precision,
            self.leverage,
            stop_loss_price,
            self.risk_per_trade
        )

        position_side = PositionSide.LONG if isinstance(event, GoLongSignalReceived) else PositionSide.SHORT

        return Position(
            symbol=event.symbol,
            timeframe=event.timeframe,
            strategy=event.strategy,
            size=size,
            entry=entry_price,
            side=position_side,
            risk_reward_ratio=self.risk_reward_ratio,
            stop_loss=stop_loss_price
        )

    async def update_position_performance(self, strategy: str):
        closed_positions = await self.position_storage.filter_positions_by_strategy(strategy)

        basic = self.position_storage.basic_performance(closed_positions, self.initial_account_size, self.risk_per_trade)
        advanced = self.position_storage.advanced_performance(closed_positions, self.initial_account_size)

        await self.dispatcher.dispatch(
            PortfolioPerformanceUpdated(strategy=strategy, basic=basic, advanced=advanced)
        )

    def create_open_position_event(self, position: Position) -> Union[LongPositionOpened, ShortPositionOpened]:
        if position.side == PositionSide.LONG:
            return LongPositionOpened(
                symbol=position.symbol,
                timeframe=position.timeframe,
                size=position.size,
                entry=position.entry_price,
                stop_loss=position.stop_loss_price
            )
        else:
            return ShortPositionOpened(
                symbol=position.symbol,
                timeframe=position.timeframe,
                size=position.size,
                entry=position.entry_price,
                stop_loss=position.stop_loss_price
            )

    def can_close_position(self, position_side: PositionSide, entry: float, event: Union[ExitLongSignalReceived, ExitShortSignalReceived, RiskThresholdBreached], profit_threshold: float = 0.05) -> bool:
        if isinstance(event, ExitLongSignalReceived) and (position_side == PositionSide.LONG):
            if entry < event.exit:
                return True

        if isinstance(event, ExitShortSignalReceived) and (position_side == PositionSide.SHORT):
            if entry > event.exit:
                return True

        if isinstance(event, RiskThresholdBreached) and (position_side == event.side):
            return True

        return False
