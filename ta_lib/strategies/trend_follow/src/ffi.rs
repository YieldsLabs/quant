use crate::{CandleMAStrategy, CrossMAStrategy, SNATRStrategy, TestingGroundStrategy};
use base::register_strategy;

fn map_to_ma(smoothing: usize) -> &'static str {
    match smoothing {
        1 => "ALMA",
        2 => "DEMA",
        3 => "EMA",
        4 => "FRAMA",
        5 => "GMA",
        6 => "HMA",
        7 => "KAMA",
        8 => "RMSMA",
        9 => "SINWMA",
        10 => "SMA",
        11 => "SMMA",
        12 => "T3",
        13 => "TEMA",
        14 => "TMA",
        15 => "VWMA",
        16 => "WMA",
        17 | _ => "ZLEMA",
    }
}

fn map_to_candle(candle: usize) -> &'static str {
    match candle {
        1 => "BOTTLE",
        2 => "DOUBLE_TROUBLE",
        3 => "GOLDEN",
        4 => "H",
        5 => "HEXAD",
        6 => "HIKKAKE",
        7 => "MARUBOZU",
        8 => "MASTER_CANDLE",
        9 => "QUINTUPLETS",
        10 => "SLINGSHOT",
        11 => "THREE_CANDLES",
        12 => "THREE_METHODS",
        13 | _ => "TASUKI",
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
    let ma = map_to_ma(smoothing);

    let strategy = CrossMAStrategy::new(ma, short_period, long_period, atr_period, stop_loss_multi);
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

    let strategy = TestingGroundStrategy::new(ma, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_candlema(
    candle: usize,
    smoothing: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let candle = map_to_candle(candle);
    let ma = map_to_ma(smoothing);

    let strategy = CandleMAStrategy::new(candle, ma, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_snatr(
    atr_period: usize,
    atr_smoothing_period: usize,
    smoothing: usize,
    long_period: usize,
    stop_loss_atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let ma = map_to_ma(smoothing);

    let strategy = SNATRStrategy::new(
        atr_period,
        atr_smoothing_period,
        ma,
        long_period,
        stop_loss_atr_period,
        stop_loss_multi,
    );
    register_strategy(Box::new(strategy))
}
