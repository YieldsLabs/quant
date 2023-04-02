from dotenv import load_dotenv
import os
from analytics.performance import PerformanceStats
from market.strategy_screening import StrategyScreening

from broker.futures_bybit_broker import FuturesBybitBroker
from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from strategy.aobb_strategy import AwesomeOscillatorBBStrategy
from strategy.bollinger_engulfing_strategy import BollingerEngulfing
from strategy.engulfing_zlema_strategy import EngulfingSMA
from strategy.extreme_euphoria_bb_strategy import ExtremeEuphoriaBBStrategy
from strategy.fvg_strategy import FairValueGapStrategy
from strategy.kangaroo_tail_strategy import KangarooTailStrategy
from strategy.bollinger_engulfing_strategy import BollingerEngulfing

from risk_management.stop_loss.trailing_stop_loss_finder import TrailingStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

broker = FuturesBybitBroker(API_KEY, API_SECRET)
symbols = ['SPELLUSDT', 'ADAUSDT', 'NEARUSDT', 'XRPUSDT', 'SOLUSDT']
timeframes = [
    '1m',
    # '3m',
    # '5m'
]

lookback = 5000
lookback_period = 50
sma_period = 50
slow_sma_period = 100
initial_account_size = 1000
num_last_trades = 15
stdev_multi = 2

atr_multi = [
    0.85,
    # 1,
    # 1.5,
    2
]

risk_reward = [
    # 1.5,
    2,
    # 3,
    4,
    # 5
]

strategies = [
    EngulfingSMA(slow_sma_period=slow_sma_period),
    BollingerEngulfing(sma_period=sma_period, multiplier=stdev_multi),
    ExtremeEuphoriaBBStrategy(sma_period=sma_period, multiplier=stdev_multi),
    KangarooTailStrategy(sma_period=slow_sma_period),
    AwesomeOscillatorBBStrategy(sma_period=sma_period),
    FairValueGapStrategy(slow_sma_period=slow_sma_period)
]

atrs = [ATRStopLossFinder(multiplier=atr_multi) for atr_multi in atr_multi]

stop_loss_finders = [] \
    + atrs \
    + [TrailingStopLossFinder(stop_loss_finder=atr) for atr in atrs] \
    + [LowHighStopLossFinder(stop_loss_finder=atr, lookback_period=lookback_period) for atr in atrs]

take_profit_finders = [] \
    + [RiskRewardTakeProfitFinder(risk_reward_ratio=rrr) for rrr in risk_reward]

analytics = PerformanceStats(initial_account_size=initial_account_size)

screener = StrategyScreening(
    broker=broker,
    analytics=analytics,
    symbols=symbols,
    timeframes=timeframes,
    strategies=strategies,
    stop_loss_finders=stop_loss_finders,
    take_profit_finders=take_profit_finders,
    lookback=lookback
)

results_df = screener.run()

print(results_df[['strategy', 'symbol', 'total_pnl', 'win_rate', 'total_trades']].head(10))
print(results_df[['strategy', 'stop_loss_finder', 'take_profit_finder']].head(10))