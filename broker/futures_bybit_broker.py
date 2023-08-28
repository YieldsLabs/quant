import ccxt
import math
from ccxt.base.errors import RequestTimeout, NetworkError

from core.commands.broker import ClosePosition, OpenPosition, UpdateSettings
from core.event_decorators import command_handler, query_handler
from core.models.broker import PositionMode
from core.models.position import PositionSide
from core.queries.broker import GetAccountBalance, GetOpenPosition, GetSymbol, GetSymbols

from broker.retry import retry
from core.models.symbol import Symbol
from core.interfaces.abstract_broker import AbstractBroker


class FuturesBybitBroker(AbstractBroker):
    def __init__(self, api_key, secret):
        super().__init__()
        self.exchange = ccxt.bybit({ 'apiKey': api_key, 'secret': secret })

    @command_handler(UpdateSettings)
    def set_settings(self, command: UpdateSettings):
        is_hedged = command.position_mode != PositionMode.ONE_WAY
        symbol = command.symbol.name
        try:
            self.exchange.set_leverage(command.leverage, symbol)
            self.exchange.set_position_mode(is_hedged, symbol)
            self.exchange.set_margin_mode(command.margin_mode.value, symbol, { 'leverage': command.leverage })
        except Exception:
            pass
    
    @command_handler(OpenPosition)
    def open_position(self, command: OpenPosition):
        position = command.position
        signal = position.signal

        self._place_market_order(position.side, signal.symbol.name, position.size, None, None)

    @command_handler(ClosePosition)
    def close_position(self, command: ClosePosition):
        position = command.position
        signal = position.signal
        symbol = signal.symbol
        
        if not self._has_open_position(symbol.name):
            return

        open_position = self._get_open_position(symbol.name)

        self._create_order('market', 'sell' if open_position['position_side'] == PositionSide.LONG else 'buy', symbol.name, open_position['position_size'])

    @query_handler(GetOpenPosition)
    def get_open_position(self, query: GetOpenPosition):
        pos = self._get_open_position(query.symbol.name)
        
        return {
            'position_size': pos['position_size'],
            'entry_price': pos['entry_price'],
        }
    
    @query_handler(GetAccountBalance)
    def get_account_balance(self, query: GetAccountBalance):
        balance = self.exchange.fetch_balance()
        return float(balance['total'][query.currency])
    
    @query_handler(GetSymbols)
    def get_symbols(self, _query: GetSymbols):
        symbols = []
        markets = self.exchange.fetch_markets()
        markets = [market_info for market_info in markets if market_info['linear'] and not market_info['type'] == 'future' and market_info['settle'] == 'USDT']

        for market in markets:
            taker_fee, maker_fee, min_position_size, min_price_size, position_precision, price_precision = self._get_symbol_meta(market)
            
            symbols.append(Symbol(
                market['id'],
                taker_fee,
                maker_fee,
                min_position_size,
                min_price_size,
                position_precision,
                price_precision
            ))

        return symbols
    
    @query_handler(GetSymbol)
    def get_symbol(self, query: GetSymbol):
        return [symbol for symbol in self.get_symbols() if symbol.name == query.name][0]
    
    def get_historical_data(self, symbol, timeframe, lookback, batch_size):
        start_time = self.exchange.milliseconds() - lookback * \
            self.exchange.parse_timeframe(timeframe) * 1000

        fetched_ohlcv = 0

        while fetched_ohlcv < lookback:
            current_limit = min(lookback - fetched_ohlcv, batch_size)

            current_ohlcv = self._fetch(symbol, timeframe, start_time, current_limit)

            if not current_ohlcv:
                break

            for data in current_ohlcv:
                yield data

                fetched_ohlcv += 1

            start_time = current_ohlcv[-1][0] + \
                self.exchange.parse_timeframe(timeframe) * 1000
    
    def _get_open_position(self, symbol: str):
        positions = self.exchange.fetch_positions(symbol)

        open_positions = [position for position in positions if float(position['info']['size']) != 0.0]

        if len(open_positions) > 0:
            current_position = open_positions[0]

            return {
                'position_side': PositionSide.LONG if current_position['side'] == 'long' else PositionSide.SHORT,
                'entry_price': float(current_position['entryPrice']),
                'position_size': float(current_position['info']['size']),
                'stop_loss_price': float(current_position['info']['stopLoss']),
                'take_profit_price': float(current_position['info']['takeProfit']),
            }

        return None
    
    def _has_open_position(self, symbol):
        return self._get_open_position(symbol) is not None
    
    def _place_market_order(self, side, symbol, position_size, stop_loss_price=None, take_profit_price=None):
        order_params = self._create_order_params('market', side, symbol, position_size)
        order_params['extra_params'] = self._create_extra_params(stop_loss_price, take_profit_price)

        res = self._create_order(**order_params)

        return res['info']['orderId']

    def _place_limit_order(self, order_side, symbol, entry_price, position_size, stop_loss_price=None, take_profit_price=None):
        order_params = self._create_order_params('limit', order_side, symbol, position_size)
        order_params.update({
            'price': entry_price,
            'extra_params': self._create_extra_params(stop_loss_price, take_profit_price)
        })

        res = self._create_order(**order_params)

        return res['info']['orderId']

    def _create_order(self, order_type, side, symbol, position_size, price=None, extra_params=None):
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

    def _create_order_params(self, order_type, side, symbol, position_size):
        return {
            'order_type': order_type,
            'side': side,
            'symbol': symbol,
            'position_size': position_size,
            'extra_params': None,
        }

    def _create_extra_params(self, stop_loss_price, take_profit_price):
        extra_params = {}

        if stop_loss_price:
            extra_params['stopLoss'] = str(stop_loss_price)

        if take_profit_price:
            extra_params['takeProfit'] = str(take_profit_price)

        if extra_params:
            extra_params['timeInForce'] = 'PostOnly'

        return extra_params if extra_params else None
    
    def _get_symbol_meta(self, market):
        taker_fee = market.get('taker', 0)
        maker_fee = market.get('maker', 0)
        
        limits = market.get('limits', {})
        min_position_size = limits.get('amount', {}).get('min', 0)
        min_position_price = limits.get('price', {}).get('min', 0)

        precision = market.get('precision', {})
        position_precision = precision.get('amount', 0)
        price_precision = precision.get('price', 0)

        return taker_fee, maker_fee, min_position_size, min_position_price, int(abs(math.log10(position_precision))), int(abs(math.log10(price_precision)))

    @retry(max_retries=7, handled_exceptions=(RequestTimeout, NetworkError))
    def _fetch(self, symbol, timeframe, start_time, current_limit):
        return self.exchange.fetch_ohlcv(
            symbol, timeframe, since=start_time, limit=current_limit)

