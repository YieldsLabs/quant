use base::prelude::*;
use candlestick::{
    bottle, double_trouble, golden, h, hexad, hikkake, marubozu, master_candle, quintuplets,
    slingshot, tasuki, three_candles, three_methods, three_one_two,
};
use core::prelude::*;

pub enum TrendCandleType {
    BOTTLE,
    DOUBLE_TROUBLE,
    GOLDEN,
    H,
    HEXAD,
    HIKKAKE,
    MARUBOZU,
    MASTER_CANDLE,
    QUINTUPLETS,
    SLINGSHOT,
    THREE_CANDLES,
    THREE_METHODS,
    TASUKI,
    THREE_ONE_TWO,
}

pub fn trend_candle_indicator(
    candle: &TrendCandleType,
    data: &OHLCVSeries,
) -> (Series<bool>, Series<bool>) {
    match candle {
        TrendCandleType::BOTTLE => (
            bottle::bullish(&data.open, &data.low, &data.close),
            bottle::bearish(&data.open, &data.high, &data.close),
        ),
        TrendCandleType::DOUBLE_TROUBLE => (
            double_trouble::bullish(&data.open, &data.high, &data.low, &data.close),
            double_trouble::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::GOLDEN => (
            golden::bullish(&data.open, &data.high, &data.low, &data.close),
            golden::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::H => (
            h::bullish(&data.open, &data.high, &data.low, &data.close),
            h::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::HEXAD => (
            hexad::bullish(&data.open, &data.high, &data.close),
            hexad::bearish(&data.open, &data.low, &data.close),
        ),
        TrendCandleType::HIKKAKE => (
            hikkake::bullish(&data.open, &data.high, &data.low, &data.close),
            hikkake::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::MARUBOZU => (
            marubozu::bullish(&data.open, &data.high, &data.low, &data.close),
            marubozu::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::MASTER_CANDLE => (
            master_candle::bullish(&data.open, &data.high, &data.low, &data.close),
            master_candle::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::QUINTUPLETS => (
            quintuplets::bullish(&data.open, &data.close),
            quintuplets::bearish(&data.open, &data.close),
        ),
        TrendCandleType::SLINGSHOT => (
            slingshot::bullish(&data.open, &data.high, &data.low, &data.close),
            slingshot::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::THREE_CANDLES => (
            three_candles::bullish(&data.open, &data.close),
            three_candles::bearish(&data.open, &data.close),
        ),
        TrendCandleType::THREE_METHODS => (
            three_methods::bullish(&data.open, &data.high, &data.low, &data.close),
            three_methods::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
        TrendCandleType::TASUKI => (
            tasuki::bullish(&data.open, &data.close),
            tasuki::bearish(&data.open, &data.close),
        ),
        TrendCandleType::THREE_ONE_TWO => (
            three_one_two::bullish(&data.open, &data.high, &data.low, &data.close),
            three_one_two::bearish(&data.open, &data.high, &data.low, &data.close),
        ),
    }
}
