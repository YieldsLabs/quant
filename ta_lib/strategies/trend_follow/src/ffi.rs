use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::filter_mapper::{map_to_filter, FilterConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use base::register_strategy;
use shared::{MovingAverageType, RSIType, TrendCandleType};

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
        17 => MovingAverageType::ZLEMA,
        _ => MovingAverageType::SMA,
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
        13 => TrendCandleType::TASUKI,
        _ => TrendCandleType::THREE_CANDLES,
    }
}

#[no_mangle]
pub fn register_cross3ma(
    smoothing: f32,
    short_period: f32,
    medium_period: f32,
    long_period: f32,
    atr_period: f32,
    atr_factor: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing as usize);
    let signal = map_to_signal(SignalConfig::Cross3Ma {
        smoothing,
        short_period,
        medium_period,
        long_period,
    });
    let filter = map_to_filter(FilterConfig::Dumb {
        period: long_period,
    });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: atr_factor,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_crosstii(
    major_period: f32,
    minor_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::CrossTII {
        major_period,
        minor_period,
        lower_barrier,
        upper_barrier,
    });
    let filter = map_to_filter(FilterConfig::Ma { smoothing, period });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_crossrsin(
    rsi_period: f32,
    threshold: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let rsi_type = RSIType::RSI;
    let signal = map_to_signal(SignalConfig::CrossRsiNeutrality {
        rsi_type,
        rsi_period,
        threshold,
    });
    let filter = map_to_filter(FilterConfig::Dumb { period: rsi_period });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_rsivma(
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let rsi_type = RSIType::RSI;
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::RsiV {
        rsi_type,
        rsi_period,
        lower_barrier,
        upper_barrier,
    });
    let filter = map_to_filter(FilterConfig::Ma { smoothing, period });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_rsi2ma(
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    short_period: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let rsi_type = RSIType::RSI;
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::Rsi2Ma {
        rsi_type,
        rsi_period,
        lower_barrier,
        upper_barrier,
        smoothing,
        short_period,
        long_period,
    });
    let filter = map_to_filter(FilterConfig::Dumb {
        period: long_period,
    });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_ground(
    smoothing: f32,
    smoothing_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::Testground {
        smoothing,
        smoothing_period,
    });
    let filter = map_to_filter(FilterConfig::Dumb {
        period: smoothing_period,
    });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_candlet(
    candle: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let candle = map_to_candle(candle as usize);
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::Trendcandle { candle });
    let filter = map_to_filter(FilterConfig::Ma { smoothing, period });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}

#[no_mangle]
pub fn register_snatr(
    atr_period: f32,
    atr_smoothing_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    stop_loss_atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    let smoothing = map_to_ma(smoothing as usize);

    let signal = map_to_signal(SignalConfig::SnAtr {
        atr_period,
        atr_smoothing_period,
        lower_barrier,
        upper_barrier,
    });
    let filter = map_to_filter(FilterConfig::Ma { smoothing, period });
    let stoploss = map_to_stoploss(StopLossConfig::Atr {
        period: stop_loss_atr_period,
        multi: stop_loss_multi,
    });
    let exit = map_to_exit(ExitConfig::Dumb {});

    register_strategy(signal, filter, stoploss, exit)
}
