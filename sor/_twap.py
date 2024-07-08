from asyncio import sleep

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.symbol import Symbol


class TWAP:
    def __init__(self, config_service: AbstractConfig):
        self.config = config_service.get("position")

    async def next_value(self, symbol: Symbol, exchange: AbstractExchange):
        current_time = 0
        timepoints = []
        twap_duration = self.config["twap_duration"]

        while current_time < twap_duration:
            bids, ask = self._fetch_book(symbol, exchange)

            timepoints.append((bids[:, 0], ask[:, 0], bids[:, 1], ask[:, 1]))

            time_interval = self._volatility_time_interval(timepoints)
            current_time += time_interval

            yield self._twap(timepoints)

            await sleep(time_interval)

    def _fetch_book(self, symbol: Symbol, exchange: AbstractExchange):
        bids, asks = exchange.fetch_order_book(symbol, depth=self.config["depth"])
        return np.array(bids), np.array(asks)

    @staticmethod
    def _twap(order_book):
        bid_prices, ask_prices, bid_volume, ask_volume = zip(*order_book)

        bid_prices, ask_prices = np.array(bid_prices), np.array(ask_prices)
        bid_volume, ask_volume = np.array(bid_volume), np.array(ask_volume)

        total_bid_volume, total_ask_volume = np.sum(bid_volume), np.sum(ask_volume)

        bid_weighted_average = np.sum(bid_prices * bid_volume) / total_bid_volume
        ask_weighted_average = np.sum(ask_prices * ask_volume) / total_ask_volume

        spread = np.mean(ask_prices - bid_prices)

        return (bid_weighted_average + ask_weighted_average) / 2.0 + 0.01 * spread

    @staticmethod
    def _volatility_time_interval(timepoints):
        high_prices = np.concatenate([ask_prices for _, ask_prices, _, _ in timepoints])
        low_prices = np.concatenate([bid_prices for bid_prices, _, _, _ in timepoints])

        high_low = np.log(high_prices / low_prices)
        volatility = np.sqrt((1 / (4 * np.log(2))) * np.mean(high_low**2))

        base_interval = 1.236
        volatility_factor = 30.0

        return base_interval + np.tanh(volatility_factor * volatility)
