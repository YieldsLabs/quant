use candlestick::{
    bottle, doji, double_trouble, engulfing, euphoria, golden, h, hexad, hikkake, kangaroo_tail,
    marubozu, master_candle, quintuplets, r, slingshot, split, tasuki, three_candles,
    three_methods, three_one_two,
};
use core::prelude::*;
use timeseries::prelude::*;

#[derive(Copy, Clone)]
pub enum CandleTrendType {
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

pub fn candlestick_trend_indicator(
    candle: &CandleTrendType,
    data: &OHLCVSeries,
) -> (Series<bool>, Series<bool>) {
    match candle {
        CandleTrendType::BOTTLE => (
            bottle::bullish(data.open(), data.low(), data.close()),
            bottle::bearish(data.open(), data.high(), data.close()),
        ),
        CandleTrendType::DOUBLE_TROUBLE => (
            double_trouble::bullish(data.open(), data.high(), data.low(), data.close()),
            double_trouble::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::GOLDEN => (
            golden::bullish(data.open(), data.high(), data.low(), data.close()),
            golden::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::H => (
            h::bullish(data.open(), data.high(), data.low(), data.close()),
            h::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::HEXAD => (
            hexad::bullish(data.open(), data.high(), data.close()),
            hexad::bearish(data.open(), data.low(), data.close()),
        ),
        CandleTrendType::HIKKAKE => (
            hikkake::bullish(data.open(), data.high(), data.low(), data.close()),
            hikkake::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::MARUBOZU => (
            marubozu::bullish(data.open(), data.high(), data.low(), data.close()),
            marubozu::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::MASTER_CANDLE => (
            master_candle::bullish(data.open(), data.high(), data.low(), data.close()),
            master_candle::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::QUINTUPLETS => (
            quintuplets::bullish(data.open(), data.close()),
            quintuplets::bearish(data.open(), data.close()),
        ),
        CandleTrendType::SLINGSHOT => (
            slingshot::bullish(data.open(), data.high(), data.low(), data.close()),
            slingshot::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::THREE_CANDLES => (
            three_candles::bullish(data.open(), data.close()),
            three_candles::bearish(data.open(), data.close()),
        ),
        CandleTrendType::THREE_METHODS => (
            three_methods::bullish(data.open(), data.high(), data.low(), data.close()),
            three_methods::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleTrendType::TASUKI => (
            tasuki::bullish(data.open(), data.close()),
            tasuki::bearish(data.open(), data.close()),
        ),
        CandleTrendType::THREE_ONE_TWO => (
            three_one_two::bullish(data.open(), data.high(), data.low(), data.close()),
            three_one_two::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
    }
}

#[derive(Copy, Clone)]
pub enum CandleReversalType {
    DOJI,
    ENGULFING,
    EUPHORIA,
    KANGAROO,
    R,
    SPLIT,
}

pub fn candlestick_reversal_indicator(
    candle: &CandleReversalType,
    data: &OHLCVSeries,
) -> (Series<bool>, Series<bool>) {
    match candle {
        CandleReversalType::DOJI => (
            doji::bullish(data.open(), data.close()),
            doji::bearish(data.open(), data.close()),
        ),
        CandleReversalType::ENGULFING => (
            engulfing::bullish(data.open(), data.high(), data.low(), data.close()),
            engulfing::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleReversalType::EUPHORIA => (
            euphoria::bullish(data.open(), data.close()),
            euphoria::bearish(data.open(), data.close()),
        ),
        CandleReversalType::KANGAROO => (
            kangaroo_tail::bullish(data.open(), data.high(), data.low(), data.close()),
            kangaroo_tail::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
        CandleReversalType::R => (
            r::bullish(data.low(), data.close()),
            r::bearish(data.high(), data.close()),
        ),
        CandleReversalType::SPLIT => (
            split::bullish(data.open(), data.high(), data.low(), data.close()),
            split::bearish(data.open(), data.high(), data.low(), data.close()),
        ),
    }
}
