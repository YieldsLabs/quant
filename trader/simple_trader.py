from typing import List, Type
from analytics.abstract_performace import AbstractPerformance
from broker.abstract_broker import AbstractBroker
from risk_management.abstract_risk_manager import AbstractRiskManager
from shared.ohlcv_context import OhlcvContext, update_ohlcv_data
from shared.order import Order
from strategy.abstract_strategy import AbstractStrategy
from trader.abstract_trader import AbstractTrader
from shared.position_side import PositionSide
from shared.order_side import OrderSide

class SimpleTrader(AbstractTrader):
    def __init__(self, ohlcv: Type[OhlcvContext], broker: Type[AbstractBroker], rm: Type[AbstractRiskManager], analytics: Type[AbstractPerformance], lookback=100):
        super().__init__(ohlcv)
        self.broker = broker
        self.rm = rm
        self.analytics = analytics
        self.completed_orders: List[Order] = []
        self.lookback = lookback
        self.reset_position_values()

    @update_ohlcv_data
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: str) -> None:
        data = self.ohlcv_context.ohlcv

        buy_signal, sell_signal = strategy.entry(data)

        print(f"buy_signal={buy_signal}, sell_signal={sell_signal}")

        current_row = data.iloc[-1]

        self.sync_and_update_positions(symbol, current_row)
        self.check_and_execute_trades(
            strategy, symbol, timeframe, current_row, buy_signal, sell_signal)
        self.print_statistics()

    def check_and_execute_trades(self, strategy, symbol, timeframe, current_row, buy_signal, sell_signal):
        if self.position_side is None:
            self.print_trade_info(strategy, symbol, timeframe, current_row)

        if buy_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(PositionSide.LONG, symbol, current_row)

        if sell_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(PositionSide.SHORT, symbol, current_row)

    def execute_trade(self, trade_side, symbol, current_row):
        self.position_side = trade_side
        self.entry_price = current_row['close']
        self.place_trade_orders(symbol)

    def place_trade_orders(self, symbol):
        market_order_side = OrderSide.BUY if self.position_side == PositionSide.LONG else OrderSide.SELL
       
        stop_loss_price, take_profit_price = self.rm.calculate_prices(
            self.position_side, self.entry_price)
        
        balance = self.broker.get_account_balance()
        
        self.position_size = self.rm.calculate_position_size(
            balance, self.entry_price, stop_loss_price)

        self.stop_loss_price = stop_loss_price
        self.take_profit_price = take_profit_price

        self.print_trade_summary(self.position_side, self.entry_price,
                                 self.position_size, self.stop_loss_price, self.take_profit_price)

        self.current_order_id = self.broker.place_limit_order(market_order_side.value, symbol, self.entry_price, self.position_size,
                                      stop_loss_price=self.stop_loss_price, take_profit_price=self.take_profit_price)

    def print_trade_summary(self, position_side, entry_price, position_size, stop_loss_price, take_profit_price):
        print(f"Go {position_side.value}")
        print(f"Entry price {entry_price}")
        print(f"Position size {position_size}")
        print(f"Stop loss {stop_loss_price}")
        print(f"Take profit {take_profit_price}")

    def sync_and_update_positions(self, symbol, current_row):
        if self.position_side is None and self.broker.has_open_position(symbol):
            self.sync_position_with_broker(symbol)
        else:
            self.update_positions(symbol, current_row)

    def sync_position_with_broker(self, symbol):
        print('Sync position with broker')
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
            print("Close position")
            self.broker.close_position(symbol)
            close_price = current_row['close']
            timestamp = current_row['timestamp']
            
            profit = self.rm.calculate_profit(self.position_side, self.position_size, self.entry_price, close_price, self.take_profit_price, self.stop_loss_price) 
            
            self.completed_orders.append(Order(timestamp, self.position_side, self.entry_price, close_price, self.stop_loss_price, self.take_profit_price, profit))
            
            self.reset_position_values()

    def update_trailing_stop_loss(self, symbol):
        stop_loss_price, _ = self.rm.calculate_prices(self.position_side, self.entry_price)

        if self.stop_loss_price != stop_loss_price:
            print(f"A new stop_loss={stop_loss_price}")
            # self.broker.update_stop_loss(self.current_order_id, symbol, self.position_side, stop_loss_price)
            # self.stop_loss_price = stop_loss_price
    
    def reset_position_values(self):
        self.position_side = None
        self.entry_price = None
        self.position_size = None
        self.stop_loss_price = None
        self.take_profit_price = None
        self.current_order_id = None

    def print_trade_info(self, strategy, symbol, timeframe, current_row):
        print(f"-------------------------------------------->")
        print(
            f"{strategy} with {self.rm.stop_loss_finder} and {self.rm.take_profit_finder} is looking for trade, {symbol} {timeframe}, price: {current_row['close']}")
        for side in [PositionSide.LONG, PositionSide.SHORT]:
            stop_loss_price, take_profit_price = self.rm.calculate_prices(
                side, current_row['close'])
            print(
                f"Side {side.value} stop_loss_price={stop_loss_price}, take_profit_price={take_profit_price}")

    def print_statistics(self):
        if self.position_side:
            print(f"Current side: {self.position_side.value}")
            print(f"Current entry price: {self.entry_price}")
            print(f"Current size: {self.position_size}")
            print(f"Current stop loss: {self.stop_loss_price}")
            print(f"Current take profit: {self.take_profit_price}")
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
