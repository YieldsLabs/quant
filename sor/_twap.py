import asyncio

import numpy as np

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractRestExchange
from core.models.symbol import Symbol


class TWAP:
    def __init__(self, config_service: AbstractConfig):
        self.config = config_service.get("order")

    async def next_value(self, symbol: Symbol, exchange: AbstractRestExchange):
        current_time = 0
        timepoints = []
        intensities = []

        while current_time < self.config.get("twap_duration", 10):
            bids, ask = await self._fetch_book(symbol, exchange)

            timepoints.append((bids[:, 0], ask[:, 0], bids[:, 1], ask[:, 1]))

            intensities += self._calculate_intensity(timepoints)

            time_interval = self._volatility_time_interval(timepoints, intensities)
            current_time += time_interval

            yield self._twap(timepoints)

            await asyncio.sleep(time_interval)

    async def _fetch_book(self, symbol: Symbol, exchange: AbstractRestExchange):
        bids, asks, _ = await asyncio.to_thread(
            exchange.fetch_order_book, symbol, self.config.get("dom", 10)
        )
        return np.array(bids), np.array(asks)

    def _volatility_time_interval(self, timepoints, intensities):
        high_prices = np.concatenate([ask_prices for _, ask_prices, _, _ in timepoints])
        low_prices = np.concatenate([bid_prices for bid_prices, _, _, _ in timepoints])

        high_low = np.log(high_prices / low_prices)
        volatility = np.sqrt((1 / (4 * np.log(2))) * np.mean(high_low**2))

        avg_intensity = np.mean(intensities) if intensities else 1.0
        dynamic_volatility_factor = (
            self.config.get("volatility_factor", 10) * avg_intensity
        )

        return np.tanh(dynamic_volatility_factor * volatility)

    def _calculate_intensity(self, timepoints):
        if not timepoints:
            return 1.0

        last_event_time = len(timepoints) - 1

        intensity = 1.0 + np.sum(
            np.exp(-self.config.get("hawkes_decay", 0.1) * np.arange(last_event_time))
        )

        return intensity

    @staticmethod
    def _twap(order_book):
        bid_prices, ask_prices, bid_volume, ask_volume = zip(*order_book)

        bid_prices, ask_prices = np.array(bid_prices), np.array(ask_prices)
        bid_volume, ask_volume = np.array(bid_volume), np.array(ask_volume)

        total_bid_volume, total_ask_volume = np.sum(bid_volume), np.sum(ask_volume)

        bid_weighted_average = np.sum(bid_prices * bid_volume) / total_bid_volume
        ask_weighted_average = np.sum(ask_prices * ask_volume) / total_ask_volume

        mid_price = (bid_weighted_average + ask_weighted_average) / 2.0

        spread, volatility = TWAP._calculate_volatility_spread(
            bid_prices, ask_prices, bid_volume, ask_volume
        )

        adj_spread = spread * volatility

        bid_price = mid_price - adj_spread / 2.0
        ask_price = mid_price + adj_spread / 2.0

        return bid_price, ask_price

    @staticmethod
    def _calculate_volatility_spread(bid_prices, ask_prices, bid_volume, ask_volume):
        diff = ask_prices - bid_prices
        spread = np.mean(diff)

        total_volume = bid_volume + ask_volume
        vol_weighted = np.sum(diff**2 * total_volume) / np.sum(total_volume)
        volatility = np.sqrt(vol_weighted)

        return spread, volatility
