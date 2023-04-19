import inspect
import json
from typing import List, Type
from analytics.abstract_analytics import AbstractAnalytics
from broker.abstract_broker import AbstractBroker
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.event_dispatcher import register_handler
from core.events.portfolio import BestStrategyEvent
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from labels.parse_label import parse_meta_label
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager
from strategy.abstract_strategy import AbstractStrategy
from strategy.strategy_manager import StrategyManager
from system.abstract_system import AbstractSystem
from optimization.backtest import Backtest
from trader.live_trader import LiveTrader
from trader.paper_trader import PaperTrader


class TradingSystem(AbstractSystem):
    def __init__(self, datasource: Type[AbstractDatasource], broker: Type[AbstractBroker], analytics: Type[AbstractAnalytics], symbols: List[str], timeframes: List[Timeframe], strategies: List[AbstractStrategy], leverage=1, lookback=5000, risk_per_trade=0.001):
        super().__init__()
        self.datasource = datasource
        self.broker = broker
        self.symbols = symbols
        self.timeframes = timeframes
        self.strategies = strategies
        
        self.leverage = leverage
        self.lookback = lookback

        self.portfolio_manager = PortfolioManager(datasource, analytics, risk_per_trade)
        self.risk_manager = RiskManager(trailing_stop_loss=False)
        
        self.trader = None
        self.backtest = None
        self.strategy_manager = None
        self.ws = None

    @register_handler(BestStrategyEvent)
    async def _on_best_strategy(self, event: BestStrategyEvent):
        strategy_id = event.id
        
        symbol, timeframe, strategy, _, take_profit = parse_meta_label(strategy_id)
        
        strategy_map = {cls.NAME: cls for cls in self.strategies if cls.NAME is not None}
        timeframe_map = {'1m': Timeframe.ONE_MINUTE, '3m': Timeframe.THREE_MINUTES, '5m': Timeframe.FIVE_MINUTES}
        
        timeframe = timeframe_map[timeframe]
        cls = strategy_map[strategy[0]]
        args = strategy[1] + take_profit[1]

        args_num = len(inspect.getfullargspec(cls).args) - 1
        
        strategy_instance = cls(*args[:args_num])
        
        await self.run_trading(symbol, timeframe, strategy_instance)

    def start(self):
        self.run_backtest()

    def run_backtest(self):
        self.backtest = Backtest(self.datasource)
        self.strategy_manager = StrategyManager([cls() for cls in self.strategies])
        self.trader = PaperTrader()
        self.backtest.run(self.symbols, self.timeframes, lookback=self.lookback)
    
    async def run_trading(self, symbol, timeframe, strategy_instance):
        self.backtest = None
        
        if not strategy_instance:
            raise ValueError("Strategy should be defined")

        if self.ws is None:
            raise ValueError("WS should be defined")
        
        self.broker.set_leverage(symbol, self.leverage)
        self.broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
        self.broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=self.leverage)
        
        self.strategy_manager = StrategyManager([strategy_instance])

        invervals = {
            Timeframe.ONE_MINUTE: 1,
            Timeframe.THREE_MINUTES: 3,
            Timeframe.FIVE_MINUTES: 5,
            Timeframe.FIFTEEN_MINUTES: 15,
            Timeframe.ONE_HOUR: 60,
            Timeframe.FOUR_HOURS: 240,
        }

        channels = [f"kline.{invervals[timeframe]}.{symbol}"]
        
        for channel in channels:
            await self.ws.send(json.dumps({"op": "subscribe", "args": [channel]}))

        # self.trader = LiveTrader(self.broker)

    def on_new_candle(self, message):
        print(message)

    def subscribe_candle_stream(self, ws):
        self.ws = ws

    def unsubscibe_candle_stream(self):
        self.ws = None
