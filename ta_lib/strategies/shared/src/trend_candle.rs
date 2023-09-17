use base::OHLCVSeries;
use candlestick::three_candles;
use core::series::Series;

pub fn trend_candle(candle: &str, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
    match candle {
        "THREE_CANDLES" => (
            three_candles::bullish(&data.open, &data.close),
            three_candles::bearish(&data.open, &data.close),
        ),
        _ => (Series::empty(1), Series::empty(1)),
    }
}
