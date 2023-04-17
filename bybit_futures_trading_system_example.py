from abc import abstractmethod
from typing import List, Type
from dotenv import load_dotenv
import os
import websocket
import json
from broker.futures_bybit_broker import FuturesBybitBroker
from core.abstract_event_manager import AbstractEventManager
from core.event_dispatcher import register_handler
from core.events.order import FillOrder
from core.events.portfolio import CheckExitConditions, PortfolioPerformanceEvent
from core.events.position import ClosedPosition, OpenLongPosition, OpenShortPosition
from core.events.strategy import GoLong, GoShort
from datasource.abstract_datasource import AbstractDatasource
from datasource.bybit_datasource import BybitDataSource
from optimization.hyperparameters import strategy_hyperparameters, stoploss_hyperparameters, takeprofit_hyperparameters
from portfolio_management.portfolio_manager import PortfolioManager
from core.timeframes import Timeframes
from risk_management.risk_manager import RiskManager
from strategies.aobb_strategy import AwesomeOscillatorBollingerBands
from strategies.bollinger_engulfing_strategy import BollingerBandsEngulfing
from strategies.engulfing_zlema_strategy import EngulfingZLMA
from strategies.extreme_euphoria_bb_strategy import ExtremeEuphoriaBollingerBands
from strategies.fvg_strategy import FairValueGapZLMA
from strategies.kangaroo_tail_strategy import KangarooTailZLMA
from strategy.abstract_strategy import AbstractStrategy
from strategy.strategy_manager import StrategyManager
from trader.backtester import Backtester
from trader.simple_trader import SimpleTrader

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

symbols = [
    'NEARUSDT',
    'SOLUSDT',
    'AVAXUSDT',
    'XRPUSDT'
]

timeframes = [
    Timeframes.ONE_MINUTE,
    Timeframes.THREE_MINUTES,
    Timeframes.FIVE_MINUTES
]

strategies = [
    AwesomeOscillatorBollingerBands,
    BollingerBandsEngulfing,
    EngulfingZLMA,
    ExtremeEuphoriaBollingerBands,
    FairValueGapZLMA,
    KangarooTailZLMA
]

search_space = {
    **strategy_hyperparameters,
    **stoploss_hyperparameters,
    **takeprofit_hyperparameters
}

class Journal(AbstractEventManager):
    def __init__(self):
        super().__init__()

    @register_handler(PortfolioPerformanceEvent)
    def _portfolio_performance(self, event: PortfolioPerformanceEvent):
        print('---------------------------------------------------->')
        print(event)

    @register_handler(FillOrder)
    def _fill_order(self, event: FillOrder):
        print('---------------------------------------------------->')
        print(event)

    @register_handler(ClosedPosition)
    def _closed_position(self, event: ClosedPosition):
        print('---------------------------------------------------->')
        print(event)

class AbstractTradingSystem(AbstractEventManager):
    @abstractmethod
    def start(self):
        pass

class TradingSystem(AbstractTradingSystem):
    def __init__(self, datasource: Type[AbstractDatasource], symbols: List[str], timeframes: List[Timeframes], strategies: List[AbstractStrategy], leverage=1, lookback=5000, risk_per_trade=0.00001):
        super().__init__()
        self.datasource = datasource
        self.symbols = symbols
        self.timeframes = timeframes
        self.leverage = leverage
        self.lookback = lookback

        self.portfolio_manager = PortfolioManager(datasource=datasource, risk_per_trade=risk_per_trade)
        self.risk_manager = RiskManager(trailing_stop_loss=False)
        self.strategy_manager = StrategyManager([cls() for cls in strategies])
        self.journal = Journal()
        self.trader = Backtester(datasource)

    def start(self):
        self.run_backtest()

    def run_backtest(self):
        self.trader.run(self.symbols, self.timeframes, lookback=self.lookback)
    
    def run_trading(self, symbol, timeframe):
        pass


broker = FuturesBybitBroker(API_KEY, API_SECRET)
datasource = BybitDataSource(broker)
bybit_trading_system = TradingSystem(datasource, symbols, timeframes, strategies)
bybit_trading_system.start()

# meta_label = str(best_result.head(1)['id'].iloc[0])
# symbol, _timeframe, _strategy, _stop_loss, _take_profit = parse_meta_label(meta_label)
# timeframe_map = {
#     '1m': Timeframes.ONE_MINUTE,
#     '3m': Timeframes.THREE_MINUTES,
#     '5m': Timeframes.FIVE_MINUTES
# }

# def create_map(classes):
#     return {cls.NAME: cls for cls in classes if cls.NAME is not None}

# strategy_map = create_map(strategies)
# stoploss_map = create_map(stop_loss_finders)
# takeprofit_map = create_map(take_profit_finders)

# timeframe = timeframe_map[_timeframe]
# strategy = strategy_map[_strategy[0]](*_strategy[1])
# stop_loss_finder = stoploss_map[_stop_loss[0]](*_stop_loss[1])
# take_profit_finder = takeprofit_map[_take_profit[0]](*_take_profit[1])

# broker.set_leverage(symbol, leverage)
# broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
# broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=leverage)

# rm = RiskManager(stop_loss_finder, take_profit_finder, risk_per_trade=risk_per_trade, **broker.get_symbol_info(symbol))
# trader = SimpleTrader(broker, rm, analytics)

# invervals = {
#     Timeframes.ONE_MINUTE: 1,
#     Timeframes.THREE_MINUTES: 3,
#     Timeframes.FIVE_MINUTES: 5,
#     Timeframes.FIFTEEN_MINUTES: 15,
#     Timeframes.ONE_HOUR: 60,
#     Timeframes.FOUR_HOURS: 240,
# }

# channels = [f"kline.{invervals[timeframe]}.{symbol}"]


# def on_open(ws):
#     print("WebSocket connection opened")
#     for channel in channels:
#         ws.send(json.dumps({"op": "subscribe", "args": [channel]}))


# def on_message(ws, message):
#     trader.trade(strategy, symbol, timeframe)


# def on_error(ws, error):
#     print(f"WebSocket error: {error}")


# def on_close(ws):
#     print("WebSocket connection closed")


# wss = 'wss://stream.bybit.com/v5/public/linear'

# ws = websocket.WebSocketApp(
#     wss,
#     on_open=on_open,
#     on_message=on_message,
#     on_error=on_error,
#     on_close=on_close
# )

# ws.run_forever()
