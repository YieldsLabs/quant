import logging
import math

import ccxt
from cachetools import TTLCache, cached
from ccxt.base.errors import NetworkError, RequestTimeout

from core.interfaces.abstract_exchange import AbstractExchange
from core.models.broker import MarginMode, PositionMode
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK, Lookback
from core.models.position import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

MAX_RETRIES = 5
EXCEPTIONS = (RequestTimeout, NetworkError)


logger = logging.getLogger(__name__)


class Bybit(AbstractExchange):
    def __init__(self, api_key: str, api_secret: str):
        self.connector = ccxt.bybit({"apiKey": api_key, "secret": api_secret})

    def update_symbol_settings(
        self,
        symbol: Symbol,
        position_mode: PositionMode,
        margin_mode: MarginMode,
        leverage: int,
    ):
        is_hedged = position_mode != PositionMode.ONE_WAY
        try:
            self.connector.set_leverage(leverage, symbol.name)
            self.connector.set_position_mode(is_hedged, symbol.name)
            self.connector.set_margin_mode(
                margin_mode.value, symbol.name, {"leverage": leverage}
            )
        except Exception as e:
            logger.error(e)
            pass

    def open_market_position(self, symbol: Symbol, side: PositionSide, size: float):
        position = self.fetch_position(symbol)

        if position:
            return None

        res = self._create_order(
            "market", "buy" if side == PositionSide.LONG else "sell", symbol.name, size
        )

        return res["info"]["orderId"]

    def close_position(self, symbol: Symbol):
        position = self.fetch_position(symbol)

        if not position:
            return None

        self._create_order(
            "market",
            "sell" if position["position_side"] == PositionSide.LONG else "buy",
            symbol.name,
            position["position_size"],
        )

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def fetch_position(self, symbol: Symbol):
        positions = self.connector.fetch_positions(symbol.name)

        open_positions = [
            position for position in positions if float(position["info"]["size"]) != 0.0
        ]

        if len(open_positions) > 0:
            current_position = open_positions[0]

            return {
                "position_side": PositionSide.LONG
                if current_position["side"] == "long"
                else PositionSide.SHORT,
                "entry_price": float(current_position["entryPrice"]),
                "position_size": float(current_position["info"]["size"]),
                "stop_loss_price": float(current_position["info"]["stopLoss"]),
                "take_profit_price": float(current_position["info"]["takeProfit"]),
            }

        return None

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def fetch_account_balance(self, currency: str):
        balance = self.connector.fetch_balance()
        return float(balance["total"][currency])

    @cached(TTLCache(maxsize=10, ttl=120))
    def fetch_symbols(self):
        markets = self._fetch_futures_market()
        symbols = [self._create_symbol(market) for market in markets]
        return symbols

    def fetch_ohlcv(
        self, symbol: Symbol, timeframe: Timeframe, lookback: Lookback, batch_size: int
    ):
        lookback = TIMEFRAMES_TO_LOOKBACK[(lookback, timeframe)]

        start_time = (
            self.connector.milliseconds()
            - lookback * self.connector.parse_timeframe(timeframe.value) * 1000
        )

        fetched_ohlcv = 0

        while fetched_ohlcv < lookback:
            current_limit = min(lookback - fetched_ohlcv, batch_size)

            current_ohlcv = self._fetch_ohlcv(
                symbol, timeframe, start_time, current_limit
            )

            if not current_ohlcv:
                break

            for data in current_ohlcv:
                yield data

                fetched_ohlcv += 1

            start_time = (
                current_ohlcv[-1][0]
                + self.connector.parse_timeframe(timeframe.value) * 1000
            )

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def _fetch_ohlcv(self, symbol, timeframe, start_time, current_limit):
        return self.connector.fetch_ohlcv(
            symbol.name, timeframe.value, since=start_time, limit=current_limit
        )

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def _fetch_futures_market(self):
        markets = self.connector.fetch_markets()

        return [
            market_info
            for market_info in markets
            if market_info["linear"]
            and market_info["type"] != "future"
            and market_info["settle"] == "USDT"
        ]

    def _create_symbol(self, market):
        (
            taker_fee,
            maker_fee,
            min_position_size,
            min_price_size,
            position_precision,
            price_precision,
        ) = self._get_symbol_meta(market)

        return Symbol(
            market["id"],
            taker_fee,
            maker_fee,
            min_position_size,
            min_price_size,
            position_precision,
            price_precision,
        )

    def _get_symbol_meta(self, market):
        taker_fee = market.get("taker", 0)
        maker_fee = market.get("maker", 0)

        limits = market.get("limits", {})
        min_position_size = limits.get("amount", {}).get("min", 0)
        min_position_price = limits.get("price", {}).get("min", 0)

        precision = market.get("precision", {})
        position_precision = precision.get("amount", 0)
        price_precision = precision.get("price", 0)

        return (
            taker_fee,
            maker_fee,
            min_position_size,
            min_position_price,
            int(abs(math.log10(position_precision))),
            int(abs(math.log10(price_precision))),
        )

    def _create_order(
        self, order_type, side, symbol, position_size, price=None, extra_params=None
    ):
        order_params = {
            "symbol": symbol,
            "type": order_type,
            "side": side,
            "amount": position_size,
        }

        if price is not None:
            order_params["price"] = price

        if extra_params is not None:
            order_params["params"] = extra_params

        return self.connector.create_order(**order_params)

    def _create_order_params(self, order_type, side, symbol, position_size):
        return {
            "order_type": order_type,
            "side": side,
            "symbol": symbol,
            "position_size": position_size,
            "extra_params": None,
        }

    def _create_order_extra_params(self, stop_loss_price, take_profit_price):
        extra_params = {}

        if stop_loss_price:
            extra_params["stopLoss"] = str(stop_loss_price)

        if take_profit_price:
            extra_params["takeProfit"] = str(take_profit_price)

        if extra_params:
            extra_params["timeInForce"] = "PostOnly"

        return extra_params if extra_params else None
