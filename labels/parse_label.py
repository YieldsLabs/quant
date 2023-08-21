import re

from core.models.timeframe import Timeframe


def get_timeframe_from_string(input_string):
    for timeframe in Timeframe:
        if str(timeframe) == input_string:
            return timeframe


def parse_meta_label(label: str):
    def parse_params(params_str: str):
        return [float(p) if '.' in p else int(p) for p in params_str.split(':')]

    pattern = r"([A-Z\d]+)_(\d+[smhd])_STRTG([A-Z]+)_([\d:.]+)_STPLSS([A-Z]+)_([\d:.]+)"
    matches = re.match(pattern, label)

    symbol = matches.group(1)
    timeframe = matches.group(2)

    strategy_name = matches.group(3)
    strategy_params = parse_params(matches.group(4))

    stop_loss_name = matches.group(5)
    stop_loss_params = parse_params(matches.group(6))

    return symbol, get_timeframe_from_string(timeframe), (strategy_name.lower(), strategy_params), (stop_loss_name, stop_loss_params)
