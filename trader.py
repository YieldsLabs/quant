from enum import Enum

class TradeSide(Enum):
    LONG = "long"
    SHORT = "short"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class Trader:
    def __init__(self, broker, rm):
        self.broker = broker
        self.rm = rm
        self.position_side = None
        self.entry_price = None
        self.position_size = None
        self.stop_loss_price = None
        self.take_profit_price = None

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
        current_row = ohlcv.iloc[-1]
        buy_signal, sell_signal = strategy.entry(ohlcv)
        print(f"buy_signal={buy_signal}, sell_signal={sell_signal}")
        balance = self.broker.get_account_balance()

        self.sync_and_update_positions(symbol, current_row)
        
        if self.position_side is None:
            print(f"-------------------------------------------->")
            print(f"{strategy} with {self.rm.stop_loss_finder} and {self.rm.take_profit_finder} is looking for trade, {symbol} {timeframe}, price: {current_row['close']}")
            for side in [TradeSide.LONG, TradeSide.SHORT]:
                stop_loss_price, take_profit_price = self.rm.calculate_prices(side, current_row['close'])
                print(f"Side {side.value} stop_loss_price={stop_loss_price}, take_profit_price={take_profit_price}")
        
        if buy_signal and not self.broker.has_open_positions(symbol) and self.position_side is None:
            self.execute_long_trade(symbol, current_row, balance)
        
        if sell_signal and not self.broker.has_open_positions(symbol) and self.position_side is None:
            self.execute_short_trade(symbol, current_row, balance)
        
        if self.position_side and not self.broker.has_open_positions(symbol):
            pnl = self.calculate_pnl(current_row)
            self.update_statistics(pnl)
            self.reset_position_values()

        self.print_statistics()

    def sync_and_update_positions(self, symbol, current_row):
        if self.position_side is None and self.broker.has_open_positions(symbol):
            print('Sync postion with broker')
            
            positions = self.broker.get_open_positions(symbol)
            
            current_position = positions[0]

            self.position_side = TradeSide.LONG if current_position['side'] == 'long' else TradeSide.SHORT
            self.entry_price = float(current_position['entryPrice'])
            self.position_size = float(current_position['info']['size'])

        if self.position_side and self.rm.check_exit_conditions(self.position_side, self.entry_price, current_row):
            print("Close position")

            order_close_side = OrderSide.BUY if self.position_side.value == TradeSide.SHORT.value else OrderSide.SELL
            self.broker.place_market_order(order_close_side.value, symbol, self.position_size)
            pnl = self.calculate_pnl(current_row)
            self.update_statistics(pnl)
            self.reset_position_values()

    def execute_long_trade(self, symbol, current_row, balance):
        self.position_side = TradeSide.LONG
        self.entry_price = current_row['close']
        self.place_trade_orders(OrderSide.BUY, symbol, balance)

    def execute_short_trade(self, symbol, current_row, balance):
        self.position_side = TradeSide.SHORT
        self.entry_price = current_row['close']
        self.place_trade_orders(OrderSide.SELL, symbol, balance)

    def place_trade_orders(self, market_order_side, symbol, balance):
        stop_loss_price, take_profit_price = self.rm.calculate_prices(
            self.position_side, self.entry_price)
        self.position_size = self.rm.calculate_position_size(
            balance, self.entry_price, stop_loss_price)
        
        self.stop_loss_price = stop_loss_price
        self.take_profit_price = take_profit_price

        print(f"Go {self.position_side.value}")
        print(f"Entry price {self.entry_price}")
        print(f"Position size {self.position_size}")
        print(f"Stop loss {stop_loss_price}")
        print(f"Take profit {take_profit_price}")

        self.broker.place_market_order(market_order_side.value, symbol, self.position_size, stop_loss_price=stop_loss_price, take_profit_price=take_profit_price)
    
    def reset_position_values(self):
        self.position_side = None
        self.entry_price = None
        self.position_size = None
        self.stop_loss_price = None
        self.take_profit_price = None

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
