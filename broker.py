from enum import Enum
import ccxt
import math
import pandas as pd

class PositionMode(Enum):
    ONE_WAY = 'one way'
    HEDGED = 'hedged'

class MarginMode(Enum):
    ISOLATED = 'isolated'
    CROSS = 'cross'

class Broker:
    def __init__(self, api_key, secret):
        self.exchange = ccxt.bybit({'apiKey': api_key, 'secret': secret})

    def get_account_balance(self):
        balance = self.exchange.fetch_balance()
        return float(balance['total']['USDT'])

    def get_symbol_info(self, symbol):
        try:
            market_info = self.exchange.fetch_markets()
            symbol_info = [market for market in market_info if market['id'] == symbol and market['linear'] == True][0]
            
            position_precision = symbol_info.get('precision', {}).get('amount', 0)
            price_precision = symbol_info.get('precision', {}).get('price', 0)
            trading_fee = symbol_info.get('taker', 0) + symbol_info.get('maker', 0)

            return {
                'trading_fee': trading_fee,
                'position_precision': int(abs(math.log10(position_precision))),
                'price_precision': int(abs(math.log10(price_precision)))
            }
        except Exception as e:
            print(e)
            
            return {
                'trading_fee': None,
                'position_precision': None,
                'price_precision': None
            }
    
    def set_leverage(self, symbol, leverage=3):
        try:
            self.exchange.set_leverage(leverage, symbol)
        except Exception as e:
            print(e)

    def set_position_mode(self, symbol, mode=PositionMode.ONE_WAY):
        is_hedged = mode != PositionMode.ONE_WAY
        try:
            self.exchange.set_position_mode(is_hedged, symbol)
        except Exception as e:
            print(e)

    def set_margin_mode(self, symbol, mode=MarginMode.ISOLATED, leverage=1):
        try:
            self.exchange.set_margin_mode(mode.value, symbol, {'leverage': leverage})
        except Exception as e:
            print(e)

    def create_order(self, order_type, side, symbol, position_size, price=None, extra_params=None):
        order_params = {
            'symbol': symbol,
            'type': order_type,
            'side': side,
            'amount': position_size,
        }

        if price is not None:
            order_params['price'] = price

        if extra_params is not None:
            order_params['params'] = extra_params

        return self.exchange.create_order(**order_params)

    def place_market_order(self, side, symbol, position_size, stop_loss_price=None, take_profit_price=None):
        order_params = {
            'order_type': 'market',
            'symbol': symbol,
            'side': side,
            'position_size': position_size,
            'extra_params': None
        }

        if stop_loss_price and not take_profit_price:
            order_params['extra_params'] = {'stopLoss': str(stop_loss_price) }
        elif take_profit_price and not stop_loss_price:
            order_params['extra_params'] = { 'takeProfit': str(take_profit_price) }
        elif take_profit_price and stop_loss_price:
            order_params['extra_params'] = { 'stopLoss': str(stop_loss_price), 'takeProfit': str(take_profit_price) }

        self.create_order(**order_params)

    def place_take_profit_order(self, side, symbol, position_size, take_profit_price):
        self.create_order('limit', side, symbol,
                          position_size, take_profit_price)

    def has_open_positions(self, symbol):
        return len(self.get_open_positions(symbol)) > 0

    def close_position(self, symbol):
        open_positions = self.get_open_positions(symbol)
        
        if len(open_positions) == 0:
            return
        
        for position in open_positions:
            self.create_order('market', 'sell' if position['side'] == 'buy' else 'buy', symbol, abs(float(position['info']['size'])))

    def get_open_positions(self, symbol):
        positions = self.exchange.fetch_positions(symbol)
        return [
            position for position in positions if float(position['info']['size']) != 0
        ]

    def fetch_symbols(self):
        markets = self.exchange.fetch_markets()
        return [market_info['id'] for market_info in markets if market_info['linear']]

    def get_historical_data(self, symbol, timeframe, limit=1000):
        ohlcv = []
        start_time = self.exchange.milliseconds() - limit * \
            self.exchange.parse_timeframe(timeframe) * 1000

        while len(ohlcv) < limit:
            current_limit = min(limit - len(ohlcv), 1000)
            current_ohlcv = self.exchange.fetch_ohlcv(
                symbol, timeframe, since=start_time, limit=current_limit)
            ohlcv += current_ohlcv
            start_time = current_ohlcv[-1][0] + \
                self.exchange.parse_timeframe(timeframe) * 1000

        df = pd.DataFrame(
            ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        for column in ['open', 'high', 'low', 'close', 'volume']:
            df[column] = df[column].astype(float)

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        return df
