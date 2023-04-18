from collections import defaultdict
from typing import Dict, List, Optional, Type, Union
import numpy as np
from core.event_dispatcher import register_handler
from core.events.ohlcv import OHLCVEvent
from core.events.order import FillOrder
from core.events.portfolio import CheckExitConditions, PortfolioPerformance, PortfolioPerformanceEvent
from core.events.position import ClosedPosition, OpenLongPosition, OpenShortPosition, PositionSide
from core.events.strategy import GoLong, GoShort
from datasource.abstract_datasource import AbstractDatasource
from .abstract_portfolio_manager import AbstractPortfolioManager
from .position import Position

class PortfolioManager(AbstractPortfolioManager):
    def __init__(self, datasource: Type[AbstractDatasource], risk_per_trade: float = 0.001):
        super().__init__()
        self.datasource = datasource
        self.risk_per_trade = risk_per_trade
        self.closed_positions: List[Position] = []
        self.active_positions: Dict[str, Position] = defaultdict(dict)

    @register_handler(OHLCVEvent)
    def _on_market(self, event: OHLCVEvent):
        symbol = event.symbol
        if symbol in self.active_positions:
            position = self.active_positions[symbol]

            self.dispatcher.dispatch(CheckExitConditions(
                symbol=symbol,
                timeframe=event.timeframe,
                side=position.side,
                size=position.size,
                entry=position.entry_price,
                stop_loss=position.stop_loss_price,
                take_profit=position.take_profit_price,
                risk=self.risk_per_trade,
                ohlcv=event.ohlcv
            ))

    @register_handler(GoLong)
    def _on_go_long(self, event: GoLong):
        self.handle_position(PositionSide.LONG, event)

    @register_handler(GoShort)
    def _on_go_short(self, event: GoShort):
        self.handle_position(PositionSide.SHORT, event)
        
    @register_handler(FillOrder)
    def _on_order_filled(self, event: FillOrder):
        symbol = event.symbol

        if symbol in self.active_positions:
            self.active_positions[symbol].add_order(event.order)
    
    @register_handler(ClosedPosition)
    def _on_closed_position(self, event: ClosedPosition):
        symbol = event.symbol

        if symbol in self.active_positions:
            position = self.active_positions[symbol]
            position.close_position(event.exit_price)
            self.closed_positions.append(position)
            del self.active_positions[symbol]
    
            performance = self.calculate_performance()
            strategy_id = position.get_id()

            self.dispatcher.dispatch(PortfolioPerformanceEvent(id=strategy_id, performance=performance))

    def handle_position(self, position_side, event: Union[GoLong, GoShort]):
        if event.symbol in self.active_positions:
            return

        position = self.create_position(position_side, event)
        self.active_positions[event.symbol] = position
        self.dispatcher.dispatch(self.create_open_position_event(position_side, event))

    def create_position(self, position_side, event: Union[GoLong, GoShort]) -> Position:
        account_size = self.datasource.account_size()
        trading_fee, min_position_size, price_precision = self.datasource.fee_and_precisions(event.symbol)

        stop_loss_price = round(event.stop_loss, price_precision) if event.stop_loss else None
        take_profit_price = round(event.take_profit, price_precision) if event.take_profit else None
        size = self.calculate_position_size(account_size, event.entry, trading_fee, min_position_size, price_precision, stop_loss_price)

        return Position(symbol=event.symbol, timeframe=event.timeframe, strategy=event.strategy, size=size, entry=event.entry, side=position_side, stop_loss=stop_loss_price, take_profit=take_profit_price)

    def create_open_position_event(self, position_side: PositionSide, event: Union[GoLong, GoShort]) -> Union[OpenLongPosition, OpenShortPosition]:
        position = self.active_positions[event.symbol]

        if position_side == PositionSide.LONG:
            return OpenLongPosition(
                symbol=event.symbol,
                timeframe=event.timeframe,
                size=position.size,
                entry=position.entry_price,
                stop_loss=position.stop_loss_price,
                take_profit=position.take_profit_price
            )
        else:
            return OpenShortPosition(
                symbol=event.symbol,
                timeframe=event.timeframe,
                size=position.size,
                entry=position.entry_price,
                stop_loss=position.stop_loss_price,
                take_profit=position.take_profit_price
            )
        
    def calculate_position_size(
        self, 
        account_size: float, 
        entry_price: float, 
        trading_fee: float, 
        min_position_size: float, 
        price_precision: int, 
        stop_loss_price: Optional[float] = None
    ) -> float:
        risk_amount = self.risk_per_trade * account_size

        if stop_loss_price and entry_price:
            price_difference = abs(entry_price - stop_loss_price) * (1 + trading_fee)
        else:
            price_difference = 1

        if price_difference != 0:
            position_size = risk_amount / price_difference
        else:
            position_size = 1

        adjusted_position_size = max(position_size, min_position_size)
        rounded_position_size = round(adjusted_position_size, price_precision)

        return rounded_position_size
        
    def calculate_performance(self) -> PortfolioPerformance:
        initial_account_size = self.datasource.account_size()
        pnl = [position.calculate_pnl() for position in self.closed_positions]
        total_trades = len(self.closed_positions)
        successful_trades = sum(position.calculate_pnl() > 0 for position in self.closed_positions)
        max_drawdown = self._max_drawdown(pnl, initial_account_size) if len(pnl) else 0
        win_rate = successful_trades / total_trades if total_trades else 0

        return PortfolioPerformance(
            total_trades=total_trades,
            successful_trades=successful_trades,
            win_rate=win_rate,
            risk_of_ruin=self._risk_of_ruin(win_rate, initial_account_size),
            rate_of_return=self._rate_of_return(pnl, initial_account_size),
            total_pnl=np.sum(pnl) if len(pnl) else 0,
            average_pnl=np.mean(pnl) if len(pnl) else 0,
            sharpe_ratio=self._sharpe_ratio(pnl) if len(pnl) else 0,
            sortino_ratio=self._sortino_ratio(pnl) if len(pnl) else 0,
            profit_factor=self._profit_factor(pnl) if len(pnl) else 0,
            max_consecutive_wins=self._max_streak(pnl, True),
            max_consecutive_losses=self._max_streak(pnl, False),
            max_drawdown=max_drawdown,
            recovery_factor=self._recovery_factor(pnl, max_drawdown) if len(pnl) else 0
        )
    
    def _sharpe_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        avg_return = np.mean(pnl_array)
        std_return = np.std(pnl_array)

        return (avg_return - risk_free_rate) / std_return if std_return else 0
    
    def _sortino_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        downside_returns = pnl_array[pnl_array < 0]

        if len(downside_returns) < 2:
            return 0

        downside_std = np.std(downside_returns)

        if downside_std == 0:
            return 0
        
        avg_return = np.mean(pnl_array)
        sortino_ratio = (avg_return - risk_free_rate) / downside_std

        return sortino_ratio

    def _max_streak(self, pnl, winning: bool):
        streak = max_streak = 0
        for pnl_value in pnl:
            if (pnl_value > 0) == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        return max_streak

    def _rate_of_return(self, pnl, initial_account_size):
        account_size = initial_account_size + sum(pnl)
        return (account_size / initial_account_size) - 1
    
    def _profit_factor(self, pnl):
        pnl_array = np.array(pnl)
        gross_profit = np.sum(pnl_array[pnl_array > 0])
        gross_loss = np.abs(np.sum(pnl_array[pnl_array < 0]))

        if gross_loss == 0:
            return 0

        profit_factor = gross_profit / gross_loss
        return profit_factor

    def _max_drawdown(self, pnl, initial_account_size):
        account_size = initial_account_size
        peak = account_size
        max_drawdown = 0

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown
    
    def _recovery_factor(self, pnl, max_drawdown):
        total_profit = sum(pnl_value for pnl_value in pnl if pnl_value > 0)
        
        return total_profit / max_drawdown if max_drawdown != 0 else 0
    
    def _risk_of_ruin(self, win_rate: float, initial_account_size):
        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate
        risk_of_ruin = ((1 - (self.risk_per_trade * (1 - loss_rate / win_rate))) ** initial_account_size) * 100
        
        return risk_of_ruin