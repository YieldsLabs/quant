import re
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from strategy.abstract_strategy import AbstractStrategy


def parse_meta_label(label: str):
    def parse_params(params_str: str):
        return [float(p) if '.' in p else int(p) for p in params_str.split(':')]

    pattern = rf"([A-Z]+[A-Z\d]+)_(\d+[smhd]){AbstractStrategy.SUFFIX}([A-Z]+)([\d:.]+){AbstractStopLoss.SUFFIX}([A-Z]+)([\d:.]+){AbstractTakeProfit.SUFFIX}([A-Z]+)([\d:.]+)"
    matches = re.match(pattern, label)

    symbol = matches.group(1)
    timeframe = matches.group(2)

    strategy_name = matches.group(3)
    strategy_params = parse_params(matches.group(4))

    stop_loss_name = matches.group(5)
    stop_loss_params = parse_params(matches.group(6))

    take_profit_name = matches.group(7)
    take_profit_params = parse_params(matches.group(8))

    return symbol, timeframe, (strategy_name, strategy_params), (stop_loss_name, stop_loss_params), (take_profit_name, take_profit_params)
