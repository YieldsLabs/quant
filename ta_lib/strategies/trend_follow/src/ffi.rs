use crate::{
    CandleStrategy, CrossMAStrategy, RSIMAStrategy, RSI2xMAStrategy, SNATRStrategy,
    TestingGroundStrategy,
};
use base::register_strategy;
use filter::FilterConfig;
use shared::{MovingAverageType, TrendCandleType};
use stop_loss::StopLossConfig;

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
    smoothing: f32,
    short_period: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing as usize);
    let short_period = short_period as usize;
    let long_period = long_period as usize;
    let atr_period = atr_period as usize;

    let filter_config = FilterConfig::DUMB {
        period: long_period,
    };
    let stoploss_config = StopLossConfig::ATR {
        period: atr_period,
        multi: stop_loss_multi,
    };

    let strategy = CrossMAStrategy::new(
        smoothing,
        short_period,
        long_period,
        filter_config,
        stoploss_config,
    );
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_rsima(
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let rsi_period = rsi_period as usize;
    let smoothing = map_to_ma(smoothing as usize);
    let period = period as usize;
    let atr_period = atr_period as usize;

    let filter_config = FilterConfig::DUMB { period };
    let stoploss_config = StopLossConfig::ATR {
        period: atr_period,
        multi: stop_loss_multi,
    };

    let strategy = RSIMAStrategy::new(
        rsi_period,
        lower_barrier,
        upper_barrier,
        smoothing,
        period,
        filter_config,
        stoploss_config,
    );
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_rsi2xma(
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    short_period: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let rsi_period = rsi_period as usize;
    let smoothing = map_to_ma(smoothing as usize);
    let short_period = short_period as usize;
    let long_period = long_period as usize;
    let atr_period = atr_period as usize;

    let filter_config = FilterConfig::DUMB {
        period: long_period,
    };
    let stoploss_config = StopLossConfig::ATR {
        period: atr_period,
        multi: stop_loss_multi,
    };

    let strategy = RSI2xMAStrategy::new(
        rsi_period,
        lower_barrier,
        upper_barrier,
        smoothing,
        short_period,
        long_period,
        filter_config,
        stoploss_config,
    );
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_ground(
    smoothing: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let ma = map_to_ma(smoothing as usize);
    let long_period = long_period as usize;
    let atr_period = atr_period as usize;

    let filter_config = FilterConfig::DUMB {
        period: long_period,
    };
    let stoploss_config = StopLossConfig::ATR {
        period: atr_period,
        multi: stop_loss_multi,
    };

    let strategy = TestingGroundStrategy::new(ma, long_period, filter_config, stoploss_config);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_candle(
    candle: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let candle = map_to_candle(candle as usize);
    let smoothing = map_to_ma(smoothing as usize);
    let period = period as usize;
    let atr_period = atr_period as usize;

    let filter_config = FilterConfig::MA { smoothing, period };
    let stoploss_config = StopLossConfig::ATR {
        period: atr_period,
        multi: stop_loss_multi,
    };

    let strategy = CandleStrategy::new(candle, filter_config, stoploss_config);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_snatr(
    atr_period: f32,
    atr_smoothing_period: f32,
    smoothing: f32,
    period: f32,
    stop_loss_atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let atr_period = atr_period as usize;
    let atr_smoothing_period = atr_smoothing_period as usize;
    let smoothing = map_to_ma(smoothing as usize);
    let period = period as usize;
    let stop_loss_atr_period = stop_loss_atr_period as usize;

    let filter_config = FilterConfig::MA { smoothing, period };
    let stoploss_config = StopLossConfig::ATR {
        period: stop_loss_atr_period,
        multi: stop_loss_multi,
    };

    let strategy = SNATRStrategy::new(
        atr_period,
        atr_smoothing_period,
        filter_config,
        stoploss_config,
    );

    register_strategy(Box::new(strategy))
}
