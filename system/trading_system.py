from itertools import product
import json
from typing import List, Type
from analytics.abstract_analytics import AbstractAnalytics
from broker.abstract_broker import AbstractBroker
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.events.ohlcv import OHLCV, OHLCVEvent
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager
from strategy.abstract_strategy import AbstractStrategy
from strategy.strategy_manager import StrategyManager
from system.abstract_system import AbstractSystem
from optimization.backtest import Backtest
from trader.create_trader import create_trader

TIMEFRAMES = {
    '1': Timeframe.ONE_MINUTE,
    '3': Timeframe.THREE_MINUTES,
    '5': Timeframe.FIVE_MINUTES,
    '15': Timeframe.FIFTEEN_MINUTES,
    '60': Timeframe.ONE_HOUR,
    '240': Timeframe.FOUR_HOURS,
}


class TradingSystem(AbstractSystem):
    def __init__(self, datasource: Type[AbstractDatasource], broker: Type[AbstractBroker], analytics: Type[AbstractAnalytics], strategies: List[Type[AbstractStrategy]], symbols: List[str], timeframes: List[Timeframe], leverage=1, lookback=5000, risk_per_trade=0.001):
        super().__init__()
        self.datasource = datasource
        self.broker = broker
        self.symbols = symbols
        self.timeframes = timeframes
        self.leverage = leverage
        self.lookback = lookback

        for symbol in self.symbols:
            self.broker.set_leverage(symbol, self.leverage)
            self.broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
            self.broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=self.leverage)

        self.portfolio_manager = PortfolioManager(datasource, analytics, risk_per_trade)
        self.risk_manager = RiskManager(trailing_stop_loss=False)
        self.backtest = Backtest(datasource)
        self.strategy_manager = StrategyManager(strategies)

        self.trader = create_trader(broker, live_trading=False)

    async def start(self, cb):
        await self.run_backtest()
        await self.dispatcher.stop_workers()
        await self.dispatcher.wait()
        await self.run_trading(cb)

    async def run_backtest(self):
        await self.backtest.run(self.symbols, self.timeframes, lookback=self.lookback)

    async def run_trading(self, cb):
        self.trader = create_trader(self.broker, live_trading=False)

        timeframes_symbols = list(product(self.timeframes, self.symbols))

        await cb(timeframes_symbols)

    def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV(
            timestamp=int(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"]),
        )

        timeframe = TIMEFRAMES[interval]

        return OHLCVEvent(
            symbol=symbol,
            timeframe=timeframe,
            ohlcv=ohlcv
        )
