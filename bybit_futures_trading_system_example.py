from dotenv import load_dotenv
import os
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from optimization.hyperparameters import strategy_hyperparameters, stoploss_hyperparameters, takeprofit_hyperparameters
from core.timeframe import Timeframe
from strategies.aobb_strategy import AwesomeOscillatorBollingerBands
from strategies.bollinger_engulfing_strategy import BollingerBandsEngulfing
from strategies.engulfing_zlema_strategy import EngulfingZLMA
from strategies.extreme_euphoria_bb_strategy import ExtremeEuphoriaBollingerBands
from strategies.fvg_strategy import FairValueGapZLMA
from strategies.kangaroo_tail_strategy import KangarooTailZLMA
from system.trading_system import TradingSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

symbols = [
    'ETHUSDT',
    'NEARUSDT',
    'SOLUSDT',
    'AVAXUSDT',
    'XRPUSDT'
]

timeframes = [
    Timeframe.ONE_MINUTE,
    Timeframe.THREE_MINUTES,
    Timeframe.FIVE_MINUTES
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

lookback = 10000
risk_per_trade = 0.001

broker = FuturesBybitBroker(API_KEY, API_SECRET)
datasource = BybitDataSource(broker)
analytics = StrategyPerformance(datasource, risk_per_trade)

bybit_trading_system = TradingSystem(datasource, analytics, symbols, timeframes, strategies, lookback=lookback, risk_per_trade=risk_per_trade)
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
