use crate::{CandleStrategy, CrossMAStrategy, SNATRStrategy, TestingGroundStrategy};
use base::register_strategy;
use filter::FilterConfig;
use shared::{MovingAverageType, TrendCandleType};

fn map_to_ma(smoothing: usize) -> MovingAverageType {
    match smoothing {
        1 => MovingAverageType::ALMA,
        2 => MovingAverageType::DEMA,
        3 => MovingAverageType::EMA,
        4 => MovingAverageType::FRAMA,
        5 => MovingAverageType::GMA,
        6 => MovingAverageType::HMA,
        7 => MovingAverageType::KAMA,
        8 => MovingAverageType::RMSMA,
        9 => MovingAverageType::SINWMA,
        10 => MovingAverageType::SMA,
        11 => MovingAverageType::SMMA,
        12 => MovingAverageType::TTHREE,
        13 => MovingAverageType::TEMA,
        14 => MovingAverageType::TMA,
        15 => MovingAverageType::VWMA,
        16 => MovingAverageType::WMA,
        17 | _ => MovingAverageType::ZLEMA,
    }
}

fn map_to_candle(candle: usize) -> TrendCandleType {
    match candle {
        1 => TrendCandleType::BOTTLE,
        2 => TrendCandleType::DOUBLE_TROUBLE,
        3 => TrendCandleType::GOLDEN,
        4 => TrendCandleType::H,
        5 => TrendCandleType::HEXAD,
        6 => TrendCandleType::HIKKAKE,
        7 => TrendCandleType::MARUBOZU,
        8 => TrendCandleType::MASTER_CANDLE,
        9 => TrendCandleType::QUINTUPLETS,
        10 => TrendCandleType::SLINGSHOT,
        11 => TrendCandleType::THREE_CANDLES,
        12 => TrendCandleType::THREE_METHODS,
        13 | _ => TrendCandleType::TASUKI,
    }
}

#[no_mangle]
pub fn register_crossma(
    smoothing: usize,
    short_period: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing);

    let filter_config = FilterConfig::DUMB { period: long_period };
    let strategy = CrossMAStrategy::new(
        smoothing,
        short_period,
        long_period,
        filter_config,
        atr_period,
        stop_loss_multi,
    );
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_ground(
    smoothing: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let ma = map_to_ma(smoothing);

    let filter_config = FilterConfig::DUMB { period: long_period };
    let strategy =
        TestingGroundStrategy::new(ma, long_period, filter_config, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_candle(
    candle: usize,
    smoothing: usize,
    period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let candle = map_to_candle(candle);
    let smoothing = map_to_ma(smoothing);

    let filter_config = FilterConfig::MA { smoothing, period };

    let strategy = CandleStrategy::new(candle, filter_config, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_snatr(
    atr_period: usize,
    atr_smoothing_period: usize,
    smoothing: usize,
    period: usize,
    stop_loss_atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing);

    let filter_config = FilterConfig::MA { smoothing, period };

    let strategy = SNATRStrategy::new(
        atr_period,
        atr_smoothing_period,
        filter_config,
        stop_loss_atr_period,
        stop_loss_multi,
    );

    register_strategy(Box::new(strategy))
}
