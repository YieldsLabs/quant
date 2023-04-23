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
from strategies.aobb_strategy import AwesomeOscillatorBollingerBands
from strategies.bollinger_engulfing_strategy import BollingerBandsEngulfing
from strategies.engulfing_zlema_strategy import EngulfingZLMA
from strategies.extreme_euphoria_bb_strategy import ExtremeEuphoriaBollingerBands
from strategies.fvg_strategy import FairValueGapZLMA
from strategies.kangaroo_tail_strategy import KangarooTailZLMA
from strategy.strategy_manager import StrategyManager
from system.abstract_system import AbstractSystem
from optimization.backtest import Backtest
from trader.create_trader import create_trader

class TradingSystem(AbstractSystem):
    def __init__(self, datasource: Type[AbstractDatasource], broker: Type[AbstractBroker], analytics: Type[AbstractAnalytics], symbols: List[str], timeframes: List[Timeframe], leverage=1, lookback=5000, risk_per_trade=0.001):
        super().__init__()
        self.datasource = datasource
        self.broker = broker
        self.symbols = symbols
        self.timeframes = timeframes
        self.leverage = leverage
        self.lookback = lookback

        self.strategies = [
            AwesomeOscillatorBollingerBands,
            BollingerBandsEngulfing,
            EngulfingZLMA,
            ExtremeEuphoriaBollingerBands,
            FairValueGapZLMA,
            KangarooTailZLMA,
        ]

        for symbol in self.symbols:
            self.broker.set_leverage(symbol, self.leverage)
            self.broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
            self.broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=self.leverage)

        self.portfolio_manager = PortfolioManager(datasource, analytics, risk_per_trade)
        self.risk_manager = RiskManager(trailing_stop_loss=False)
        self.backtest = Backtest(datasource)
        self.strategy_manager = StrategyManager(self.strategies)
        self.trader = create_trader(broker, live_trading=False)
        self.ws = None


    async def start(self):
        await self.run_backtest()
        await self.dispatcher.stop_workers()
        await self.dispatcher.wait()
        await self.run_trading()

    async def run_backtest(self):
        await self.backtest.run(self.symbols, self.timeframes, lookback=self.lookback)
    
    async def run_trading(self):
        if self.ws is None:
            raise ValueError("WS should be defined")
        
        invervals = {
            Timeframe.ONE_MINUTE: 1,
            Timeframe.THREE_MINUTES: 3,
            Timeframe.FIVE_MINUTES: 5,
            Timeframe.FIFTEEN_MINUTES: 15,
            Timeframe.ONE_HOUR: 60,
            Timeframe.FOUR_HOURS: 240,
        }

        channels = [f"kline.{invervals[timeframe]}.{symbol}" for (timeframe, symbol) in list(product(self.timeframes, self.symbols))]

        for channel in channels:
            await self.ws.send(json.dumps({"op": "subscribe", "args": [channel]}))

        self.trader = create_trader(self.broker, live_trading=False)

    async def on_new_candle(self, message):
        data = message["data"][0]
        
        symbol = message["topic"].split(".")[2]
        interval = message["topic"].split(".")[1]

        timeframes = {
            '1': Timeframe.ONE_MINUTE,
            '3': Timeframe.THREE_MINUTES,
            '5': Timeframe.FIVE_MINUTES,
            '15': Timeframe.FIFTEEN_MINUTES,
            '60': Timeframe.ONE_HOUR,
            '240': Timeframe.FOUR_HOURS,
        }

        timeframe = timeframes[interval]

        ohlcv = OHLCV(
            timestamp=int(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"]),
        )

        await self.dispatcher.dispatch(OHLCVEvent(
            symbol=symbol,
            timeframe=timeframe,
            ohlcv=ohlcv
        ))

    def subscribe_candle_stream(self, ws):
        self.ws = ws

    def unsubscibe_candle_stream(self):
        self.ws = None
