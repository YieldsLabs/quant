from dotenv import load_dotenv
import os
import itertools
import pandas as pd

from backtest.backtester import Backtester
from broker.futures_bybit_broker import FuturesBybitBroker
from strategy.aobb_strategy import AwesomeOscillatorBBStrategy
from strategy.bollinger_engulfing_strategy import BollingerEngulfing
from strategy.engulfing_zlema_strategy import EngulfingSMA
from strategy.extreme_euphoria_bb_strategy import ExtremeEuphoriaBBStrategy
from strategy.kangaroo_tail_strategy import KangarooTailStrategy
from strategy.structured_duration_strategy import StructuredDurationStrategy
from strategy.bollinger_engulfing_strategy import BollingerEngulfing
from shared.trade_type import TradeType

from risk_management.risk_manager import RiskManager
from risk_management.stop_loss.trailing_stop_loss_finder import TrailingStopLossFinder
from risk_management.take_profit.noop_take_profit_finder import NoopTakeProfitFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

broker = FuturesBybitBroker(API_KEY, API_SECRET)
symbols = ['ETHUSDT', 'UNFIUSDT', 'SOLUSDT', 'XRPUSDT']
timeframes = ['1m']
row_number = 1000
lookback_period = 30
risk_reward_ratio = 1.5
atr_multi = 1.3

strategies = [
    EngulfingSMA(),
    BollingerEngulfing(),
    ExtremeEuphoriaBBStrategy(),
    # StructuredDurationStrategy(),
    KangarooTailStrategy(),
    # AwesomeOscillatorBBStrategy(),
]

stop_loss_finders = [
    TrailingStopLossFinder(atr_multiplier=atr_multi),
]

take_profit_finders = [
    # RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio),
    NoopTakeProfitFinder()
]

combinations = list(itertools.product(symbols, timeframes, strategies, stop_loss_finders, take_profit_finders))
results_list = []

for symbol, timeframe, strategy, stop_loss_finder, take_profit_finder in combinations:
    ohlcv = broker.get_historical_data(symbol, timeframe, limit=row_number)
    stop_loss_finder.set_ohlcv(ohlcv)
    market = broker.get_symbol_info(symbol)

    rm = RiskManager(stop_loss_finder, take_profit_finder, trading_fee=market['trading_fee'], price_precision=market['price_precision'], position_precision=market['position_precision'])
    backtester = Backtester(strategy, rm, ohlcv)
    
    result = backtester.run(trade_type=TradeType.BOTH)
    
    result.update({
        'symbol': symbol,
        'timeframe': timeframe,
        'strategy': strategy,
        'stop_loss_finder': stop_loss_finder,
        'take_profit_finder': take_profit_finder,
        'win_rate': result['win_rate'] * 100
    })

    results_list.append(result)
    
    print(f"{symbol} orders for strategy: {strategy}, TimeFrame: {timeframe}, StopLossFinder: {stop_loss_finder}, TakeProfitFinder: {take_profit_finder}")
    print(backtester.get_orders().head())

results_df = pd.DataFrame(results_list)
sorded_results = results_df.sort_values(by="total_pnl", ascending=False)

print(sorded_results[['strategy', 'total_pnl', 'win_rate', 'symbol', 'total_trades']].head(10))