from trader.trade_side import TradeSide
from trader.order_side import OrderSide


class SimpleTrader:
    def __init__(self, broker, rm):
        self.broker = broker
        self.rm = rm
        self.reset_position_values()
        self.initialize_statistics()

    def initialize_statistics(self):
        self.pln = 0
        self.total_trades = 0
        self.win_ratio = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        self.max_drawdown = 0
        self.current_wins = 0
        self.current_losses = 0

    def trade(self, strategy, symbol, timeframe):
        ohlcv = self.broker.get_historical_data(symbol, timeframe)
        self.rm.stop_loss_finder.set_ohlcv(ohlcv)
        buy_signal, sell_signal = strategy.entry(ohlcv)

        print(f"buy_signal={buy_signal}, sell_signal={sell_signal}")

        balance = self.broker.get_account_balance()
        current_row = ohlcv.iloc[-1]

        self.sync_and_update_positions(symbol, current_row)
        self.check_and_execute_trades(
            strategy, symbol, timeframe, current_row, buy_signal, sell_signal, balance)
        self.print_statistics()

    def check_and_execute_trades(self, strategy, symbol, timeframe, current_row, buy_signal, sell_signal, balance):
        if self.position_side is None:
            self.print_trade_info(strategy, symbol, timeframe, current_row)

        if buy_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(TradeSide.LONG, symbol, current_row, balance)

        if sell_signal and not self.broker.has_open_position(symbol):
            self.execute_trade(TradeSide.SHORT, symbol, current_row, balance)

    def execute_trade(self, trade_side, symbol, current_row, balance):
        self.position_side = trade_side
        self.entry_price = current_row['close']
        self.place_trade_orders(symbol, balance)

    def place_trade_orders(self, symbol, balance):
        market_order_side = OrderSide.BUY if self.position_side == TradeSide.LONG else OrderSide.SELL
       
        stop_loss_price, take_profit_price = self.rm.calculate_prices(
            self.position_side, self.entry_price)
        
        self.position_size = self.rm.calculate_position_size(
            balance, self.entry_price, stop_loss_price)

        self.stop_loss_price = stop_loss_price
        self.take_profit_price = take_profit_price

        self.print_trade_summary(self.position_side, self.entry_price,
                                 self.position_size, self.stop_loss_price, self.take_profit_price)

        self.broker.place_limit_order(market_order_side.value, symbol, self.entry_price, self.position_size,
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
            pnl = self.calculate_pnl(current_row)
            self.update_statistics(pnl)
            self.reset_position_values()
        elif self.rm.check_exit_conditions(self.position_side, self.entry_price, current_row):
            print("Close position")
            self.broker.close_position(symbol)
            pnl = self.calculate_pnl(current_row)
            self.update_statistics(pnl)
            self.reset_position_values()


    def reset_position_values(self):
        self.position_side = None
        self.entry_price = None
        self.position_size = None
        self.stop_loss_price = None
        self.take_profit_price = None
        self.current_order_id = None


    def update_statistics(self, pnl):
        self.pln += pnl
        self.total_trades += 1
        self.win_ratio = (self.current_wins / self.total_trades) * 100
        if pnl > 0:
            self.current_wins += 1
            self.current_losses = 0
            self.max_consecutive_wins = max(
                self.max_consecutive_wins, self.current_wins)
        else:
            self.current_losses += 1
            self.current_wins = 0
            self.max_consecutive_losses = max(
                self.max_consecutive_losses, self.current_losses)

        drawdown = self.calculate_drawdown()
        self.max_drawdown = min(self.max_drawdown, drawdown)


    def calculate_drawdown(self):
        return self.pln / self.total_trades if self.total_trades > 0 else 0


    def calculate_pnl(self, current_row):
        if self.position_side.value == TradeSide.LONG.value:
            pnl = (current_row['close'] - self.entry_price) * self.position_size
        else:
            pnl = (self.entry_price - current_row['close']) * self.position_size
        return pnl


    def print_trade_info(self, strategy, symbol, timeframe, current_row):
        print(f"-------------------------------------------->")
        print(
            f"{strategy} with {self.rm.stop_loss_finder} and {self.rm.take_profit_finder} is looking for trade, {symbol} {timeframe}, price: {current_row['close']}")
        for side in [TradeSide.LONG, TradeSide.SHORT]:
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
        print(f"Total trades: {self.total_trades}")
        print(f"Profit/Loss: {self.pln:.2f}")
        print(f"Win ratio: {self.win_ratio:.2f}%")
        print(f"Max consecutive wins: {self.max_consecutive_wins}")
        print(f"Max consecutive losses: {self.max_consecutive_losses}")
        print(f"Max drawdown: {self.max_drawdown:.2f}")
