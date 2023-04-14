from typing import List, Type
from analytics.abstract_performace import AbstractPerformance
from broker.abstract_broker import AbstractBroker
from ohlcv.context import OhlcvContext, update_ohlcv
from risk_management.abstract_risk_manager import AbstractRiskManager
from shared.order import Order
from shared.timeframes import Timeframes
from strategy.base.abstract_strategy import AbstractStrategy
from trader.abstract_trader import AbstractTrader
from shared.position_side import PositionSide
from shared.order_side import OrderSide
from trader.trade_info import TradeInfo


class SimpleTrader(AbstractTrader):
    def __init__(self, broker: Type[AbstractBroker], rm: Type[AbstractRiskManager], analytics: Type[AbstractPerformance]):
        super().__init__()
        self.broker = broker
        self.rm = rm
        self.analytics = analytics
        self.completed_orders: List[Order] = []
        self.reset_trade_values()

    @update_ohlcv
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: Timeframes) -> None:
        current_row = self.ohlcv_context.ohlcv.iloc[-1]

        self.print_trade_intro(strategy, symbol, timeframe, current_row)

        self.sync_and_update_positions(symbol, current_row)

        self.check_and_execute_trades(
            strategy, symbol, current_row)

        self.print_statistics()

    def check_and_execute_trades(self, strategy, symbol, current_row):
        buy_signal, sell_signal = strategy.entry(self.ohlcv_context.ohlcv)

        if buy_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(PositionSide.LONG, symbol, current_row)

        if sell_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(PositionSide.SHORT, symbol, current_row)

    def execute_trade(self, position_side, symbol, current_row):
        self.place_trade_orders(symbol, position_side, current_row['close'])
        self.print_trade_summary()

    def place_trade_orders(self, symbol, position_side, entry_price):
        order_side = OrderSide.BUY if position_side == PositionSide.LONG else OrderSide.SELL
        account_size = self.broker.get_account_balance()
        position_size, stop_loss_price, take_profit_price = self.rm.calculate_entry(
            position_side, account_size, entry_price)

        current_order_id = None

        if self.rm.trailing_stop_loss:
            current_order_id = self.broker.place_limit_order(order_side, symbol, entry_price, position_size,
                                                             stop_loss_price=stop_loss_price)
        else:
            current_order_id = self.broker.place_limit_order(order_side, symbol, entry_price, position_size,
                                                             stop_loss_price=stop_loss_price, take_profit_price=take_profit_price)
        if not current_order_id:
            return

        self.update_trade_values(current_order_id, position_side, entry_price,
                                 position_size, stop_loss_price, take_profit_price)

    def sync_and_update_positions(self, symbol, current_row):
        if self.position_side is None and self.broker.has_open_position(symbol):
            self.sync_position_with_broker(symbol)
        else:
            self.update_positions(symbol, current_row)

    def sync_position_with_broker(self, symbol):
        print(f'Sync {symbol} position with broker')

        current_position = self.broker.get_open_position(symbol)
        self.position_side = current_position['position_side']
        self.entry_price = current_position['entry_price']
        self.position_size = current_position['position_size']
        self.stop_loss_price = current_position['stop_loss_price']
        self.take_profit_price = current_position['take_profit_price']

    def update_positions(self, symbol, current_row):
        if not self.position_side:
            return

        if not self.broker.has_open_position(symbol):
            self.reset_position_values()
        elif self.rm.check_exit_conditions(self.position_side, self.entry_price, current_row):
            print(f"Close position {self.position_side}")

            self.broker.close_position(symbol)

            close_price = current_row['close']
            timestamp = current_row['timestamp']

            profit = self.rm.calculate_profit(self.position_side, self.position_size,
                                              self.entry_price, close_price, self.take_profit_price, self.stop_loss_price)

            self.completed_orders.append(Order(timestamp, self.position_side, self.entry_price,
                                         close_price, self.stop_loss_price, self.take_profit_price, profit, self.current_order_id))

            self.reset_trade_values()

    def reset_trade_values(self):
        self.position_side = None
        self.entry_price = None
        self.position_size = None
        self.stop_loss_price = None
        self.take_profit_price = None
        self.current_order_id = None

    def update_trade_values(self, current_order_id: str, position_side: PositionSide, entry_price: float, position_size: float, stop_loss_price: float, take_profit_price: float) -> None:
        self.current_order_id = current_order_id
        self.position_size = position_size
        self.position_side = position_side
        self.entry_price = entry_price
        self.stop_loss_price = stop_loss_price
        self.take_profit_price = take_profit_price

    def print_trade_summary(self):
        trade_info = self._get_trade_info()

        print(f"Go {trade_info.position_side}")
        print(f"Entry price {trade_info.entry_price}")
        print(f"Position size {trade_info.position_size}")
        print(f"Stop loss {trade_info.stop_loss_price}")
        print(f"Take profit {trade_info.take_profit_price}")

    def print_trade_intro(self, strategy, symbol, timeframe, current_row):
        print("-------------------------------------------->")
        print(
            f"{symbol}_{timeframe}_{current_row['close']}{strategy}{self.rm.stop_loss_finder}{self.rm.take_profit_finder}")
        for side in [PositionSide.LONG, PositionSide.SHORT]:
            stop_loss_price, take_profit_price = self.rm.calculate_prices(
                side, current_row['close'])
            print(
                f"Side {side.value} stop_loss_price={stop_loss_price}, take_profit_price={take_profit_price}")

    def print_statistics(self):
        trade_info = self._get_trade_info()

        if trade_info.position_side:
            print(f"Current side: {trade_info.position_side}")
            print(f"Current entry price: {trade_info.entry_price}")
            print(f"Current size: {trade_info.position_size}")
            print(f"Current stop loss: {trade_info.stop_loss_price}")
            print(f"Current take profit: {trade_info.take_profit_price}")
        else:
            stats = self.analytics.calculate(self.completed_orders)

            print(f"Total trades: {stats['total_trades']}")
            print(f"Successful trades: {stats['successful_trades']}")
            print(f"Win rate: {stats['win_rate']:.2%}")
            print(f"Rate of return: {stats['rate_of_return']:.2%}")
            print(f"Total PnL: {stats['total_pnl']:.2f}")
            print(f"Average PnL: {stats['average_pnl']:.2f}")
            print(f"Sharpe ratio: {stats['sharpe_ratio']:.2f}")
            print(f"Max consecutive wins: {stats['max_consecutive_wins']}")
            print(f"Max consecutive losses: {stats['max_consecutive_losses']}")
            print(f"Max drawdown: {stats['max_drawdown']:.2%}")

    def _get_trade_info(self) -> TradeInfo:
        return TradeInfo(
            position_side=self.position_side,
            entry_price=self.entry_price,
            position_size=self.position_size,
            stop_loss_price=self.stop_loss_price,
            take_profit_price=self.take_profit_price,
            current_order_id=self.current_order_id,
        )
