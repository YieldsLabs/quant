use std::fmt;
use base::OHLCVSeries;
use candlestick::{
    bottle, double_trouble, golden, h, hexad, hikkake, marubozu, master_candle, quintuplets,
    slingshot, tasuki, three_candles, three_methods,
};
use core::series::Series;

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
    TASUKI
}

impl fmt::Display for TrendCandleType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::BOTTLE => write!(f, "BOTTLE"),
            Self::DOUBLE_TROUBLE => write!(f, "DOUBLE_TROUBLE"),
            Self::GOLDEN => write!(f, "GOLDEN"),
            Self::H => write!(f, "H"),
            Self::HEXAD => write!(f, "HEXAD"),
            Self::HIKKAKE => write!(f, "HIKKAKE"),
            Self::MARUBOZU => write!(f, "MARUBOZU"),
            Self::MASTER_CANDLE => write!(f, "MASTER_CANDLE"),
            Self::QUINTUPLETS => write!(f, "QUINTUPLETS"),
            Self::SLINGSHOT => write!(f, "SLINGSHOT"),
            Self::THREE_CANDLES => write!(f, "THREE_CANDLES"),
            Self::THREE_METHODS => write!(f, "THREE_METHODS"),
            Self::TASUKI => write!(f, "TASUKI")
        }
    }
}

pub fn trend_candle(candle: &TrendCandleType, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
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
        _ => (Series::empty(1), Series::empty(1)),
    }
}
