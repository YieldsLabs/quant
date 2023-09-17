use base::OHLCVSeries;
use candlestick::{
    bottle, double_trouble, golden, h, hikkake, marubozu, master_candle, quintuplets, slingshot, tasuki,
    three_candles, three_methods,
};
use core::series::Series;

pub fn trend_candle(candle: &str, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
    match candle {
        "BOTTLE" => (
            bottle::bullish(&data.open, &data.low, &data.close),
            bottle::bearish(&data.open, &data.high, &data.close),
        ),
        "DOUBLE_TROUBLE" => (
            double_trouble::bullish(&data.open, &data.high, &data.low, &data.close),
            double_trouble::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "GOLDEN" => (
            golden::bullish(&data.open, &data.high, &data.low, &data.close),
            golden::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "H" => (
            h::bullish(&data.open, &data.high, &data.low, &data.close),
            h::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "HIKKAKE" => (
            hikkake::bullish(&data.open, &data.high, &data.low, &data.close),
            hikkake::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "MARUBOZU" => (
            marubozu::bullish(&data.open, &data.high, &data.low, &data.close),
            marubozu::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "MASTER_CANDLE" => (
            master_candle::bullish(&data.open, &data.high, &data.low, &data.close),
            master_candle::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "QUINTUPLETS" => (
            quintuplets::bullish(&data.open, &data.close),
            quintuplets::bearish(&data.open, &data.close),
        ),
        "SLINGSHOT" => (
            slingshot::bullish(&data.open, &data.high, &data.low, &data.close),
            slingshot::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "THREE_CANDLES" => (
            three_candles::bullish(&data.open, &data.close),
            three_candles::bearish(&data.open, &data.close),
        ),
        "THREE_METHODS" => (
            three_methods::bullish(&data.open, &data.high, &data.low, &data.close),
            three_methods::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        "TASUKI" => (
            tasuki::bullish(&data.open, &data.close),
            tasuki::bearish(&data.open, &data.close),
        ),
        _ => (Series::empty(1), Series::empty(1)),
    }
}
