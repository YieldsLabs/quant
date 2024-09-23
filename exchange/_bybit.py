import logging
import math
from collections import defaultdict
from datetime import datetime

import ccxt
from cachetools import TTLCache, cached
from ccxt.base.errors import NetworkError, RequestTimeout

from core.interfaces.abstract_exchange import AbstractExchange
from core.models.broker import MarginMode, PositionMode
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK, Lookback
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from infrastructure.retry import retry

MAX_RETRIES = 13
EXCEPTIONS = (RequestTimeout, NetworkError)


logger = logging.getLogger(__name__)


class Bybit(AbstractExchange):
    _instance = None

    def __new__(cls, api_key: str, api_secret: str):
        if not cls._instance:
            cls._instance = super(Bybit, cls).__new__(cls)
            cls._instance._initialize(api_key, api_secret)
        return cls._instance

    def _initialize(self, api_key: str, api_secret: str):
        self.connector = ccxt.bybit({"apiKey": api_key, "secret": api_secret})
        self.connector.load_markets()

    def update_symbol_settings(
        self,
        symbol: Symbol,
        position_mode: PositionMode,
        margin_mode: MarginMode,
        leverage: int,
    ):
        is_hedged = position_mode != PositionMode.ONE_WAY
        operations = [
            (self.connector.set_leverage, (leverage, symbol.name)),
            (self.connector.set_position_mode, (is_hedged, symbol.name)),
            (
                self.connector.set_margin_mode,
                (margin_mode.value, symbol.name, {"leverage": leverage}),
            ),
        ]

        for operation, args in operations:
            try:
                operation(*args)
            except Exception as e:
                logger.error(f"{symbol}: {e}")

    def has_filled_order(self, order_id: str, symbol: Symbol):
        try:
            orders = self.connector.fetch_closed_orders(symbol.name)
            return len([order for order in orders if order["id"] == order_id])
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def has_open_orders(
        self, symbol: Symbol, side: PositionSide, is_reduced: bool = False
    ):
        try:
            orders = self.connector.fetch_open_orders(symbol.name)

            if not is_reduced:
                order_side = "buy" if side == PositionSide.LONG else "sell"
            else:
                order_side = "sell" if side == PositionSide.LONG else "buy"

            return len(
                [
                    order
                    for order in orders
                    if not order["stopPrice"] and order["side"] == order_side
                ]
            )
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def cancel_order(self, order_id: str, symbol: Symbol):
        try:
            self.connector.cancel_order(order_id, symbol.name)
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def fetch_trade(
        self, symbol: Symbol, side: PositionSide, since: int, size: float, limit: int
    ):
        last_trades = (
            trade
            for trade in self.connector.fetch_my_trades(symbol.name, limit=limit * 2)
            if trade["timestamp"] >= since
        )

        def round_down_to_minute(timestamp):
            return datetime.utcfromtimestamp(timestamp // 1000).replace(
                second=0, microsecond=0
            )

        aggregated_trades = defaultdict(lambda: {"amount": 0, "price": 0, "fee": 0})

        opposite_side = "buy" if side == PositionSide.SHORT else "sell"

        trade_stack = sorted(
            (trade for trade in last_trades if trade["side"] == opposite_side),
            key=lambda trade: trade["timestamp"],
            reverse=True,
        )

        acc_size = 0

        for trade in trade_stack:
            if acc_size >= size:
                break

            trade_amount = trade["amount"]
            key = round_down_to_minute(trade["timestamp"])

            trade_amount = min(trade["amount"], size - acc_size)

            aggregated_trades[key]["amount"] += trade_amount
            aggregated_trades[key]["price"] += trade["price"] * trade_amount
            aggregated_trades[key]["fee"] += (
                trade["fee"]["cost"] / trade["amount"]
            ) * trade_amount

            acc_size += trade_amount

        for _, trade_data in aggregated_trades.items():
            if trade_data["amount"] > 0:
                trade_data["price"] /= trade_data["amount"]

        return next(iter(aggregated_trades.values()), None)

    def fetch_order_book(self, symbol: Symbol, depth: int = 30):
        book = self.connector.fetch_order_book(symbol.name, limit=depth)
        return book["bids"], book["asks"]

    def create_market_order(self, symbol: Symbol, side: PositionSide, size: float):
        try:
            res = self._create_order(
                "market",
                "buy" if side == PositionSide.LONG else "sell",
                symbol.name,
                size,
                extra_params=self._create_order_extra_params(side),
            )

            return res["info"]["orderId"]
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def create_limit_order(
        self, symbol: Symbol, side: PositionSide, size: float, price: float
    ):
        try:
            res = self._create_order(
                "limit",
                "buy" if side == PositionSide.LONG else "sell",
                symbol.name,
                size,
                price,
                extra_params=self._create_order_extra_params(side),
            )

            return res["info"]["orderId"]
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def create_reduce_order(
        self, symbol: Symbol, side: PositionSide, size: float, price: float
    ):
        try:
            res = self._create_order(
                "limit",
                "sell" if side == PositionSide.LONG else "buy",
                symbol.name,
                size,
                price,
                extra_params=self._create_order_extra_params(side, reduce=True),
            )

            return res["info"]["orderId"]
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def close_full_position(self, symbol: Symbol, side: PositionSide):
        position = self.fetch_position(symbol, side)

        if not position:
            return

        try:
            self._create_order(
                "market",
                "sell" if position["position_side"] == PositionSide.LONG else "buy",
                symbol.name,
                position["position_size"],
                extra_params=self._create_order_extra_params(side),
            )
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    def close_half_position(self, symbol: Symbol, side: PositionSide):
        position = self.fetch_position(symbol, side)

        if not position:
            return

        try:
            self._create_order(
                "market",
                "sell" if position["position_side"] == PositionSide.LONG else "buy",
                symbol.name,
                position["position_size"] // 2,
                extra_params=self._create_order_extra_params(side),
            )
        except Exception as e:
            logger.error(f"{symbol}: {e}")
            return

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def fetch_position(self, symbol: Symbol, side: PositionSide):
        positions = self.connector.fetch_positions([symbol.name])
        position = next(
            (p for p in positions if p["side"] == str(side).lower()),
            None,
        )

        if position and position["entryPrice"] is not None:
            return {
                "position_side": PositionSide.LONG
                if position["side"] == "long"
                else PositionSide.SHORT,
                "entry_price": float(position.get("entryPrice", 0)),
                "position_size": float(position.get("contracts", 0)),
                "open_fee": -float(position.get("info", {}).get("curRealisedPnl", 0)),
            }

        return None

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def fetch_account_balance(self, currency: str):
        balance = self.connector.fetch_balance()
        return float(balance["total"][currency])

    @cached(TTLCache(maxsize=300, ttl=120))
    def fetch_future_symbols(self):
        return [self._create_symbol(market) for market in self._fetch_futures_market()]

    def fetch_ohlcv(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        in_sample: Lookback,
        out_sample: Lookback | None,
        batch_size: int = 512,
    ):
        in_sample = TIMEFRAMES_TO_LOOKBACK[(in_sample, timeframe)]
        out_sample = (
            TIMEFRAMES_TO_LOOKBACK[(out_sample, timeframe)] if out_sample else 0
        )

        lookback = in_sample + out_sample

        start_time = (
            self.connector.milliseconds()
            - lookback * self.connector.parse_timeframe(timeframe.value) * 1000
        )

        max_time = (
            start_time
            + in_sample * self.connector.parse_timeframe(timeframe.value) * 1000
        )

        fetched_ohlcv = 0

        while fetched_ohlcv < in_sample:
            current_limit = min(in_sample - fetched_ohlcv, batch_size)

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

            if start_time >= max_time:
                break

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def _fetch_ohlcv(self, symbol, timeframe, start_time, current_limit):
        return self.connector.fetch_ohlcv(
            symbol.name, timeframe.value, since=start_time, limit=current_limit
        )

    @retry(max_retries=MAX_RETRIES, handled_exceptions=EXCEPTIONS)
    def _fetch_futures_market(self):
        return [
            market_info
            for market_info in self.connector.fetch_markets()
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
            max_leverage,
        ) = self._get_symbol_meta(market)

        return Symbol(
            market["id"],
            taker_fee,
            maker_fee,
            min_position_size,
            min_price_size,
            position_precision,
            price_precision,
            max_leverage,
        )

    def _get_symbol_meta(self, market):
        taker_fee = market.get("taker", 0)
        maker_fee = market.get("maker", 0)

        limits = market.get("limits", {})
        min_position_size = limits.get("amount", {}).get("min", 0)
        min_position_price = limits.get("price", {}).get("min", 0)
        max_leverage = limits.get("leverage", {}).get("max", 1)

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
            max_leverage,
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

    def _create_order_extra_params(
        self,
        side: PositionSide,
        reduce=False,
        stop_loss_price=None,
        take_profit_price=None,
    ):
        extra_params = {"timeInForce": "GTC"}

        extra_params["positionIdx"] = 1 if side == PositionSide.LONG else 2

        if reduce:
            extra_params["reduceOnly"] = True

        if stop_loss_price:
            extra_params["stopLoss"] = str(stop_loss_price)

        if take_profit_price:
            extra_params["takeProfit"] = str(take_profit_price)

        return extra_params
