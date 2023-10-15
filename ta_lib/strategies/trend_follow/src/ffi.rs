use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::filter_mapper::{map_to_filter, FilterConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use base::register_strategy;

fn create_and_register(
    signal: SignalConfig,
    filter: FilterConfig,
    stoploss: StopLossConfig,
    exit: ExitConfig,
) -> i32 {
    let mapped_signal = map_to_signal(signal);
    let mapped_filter = map_to_filter(filter);
    let mapped_stoploss = map_to_stoploss(stoploss);
    let mapped_exit = map_to_exit(exit);

    register_strategy(mapped_signal, mapped_filter, mapped_stoploss, mapped_exit)
}

fn read_from_memory(ptr: *const u8, len: usize) -> Vec<u8> {
    unsafe { Vec::from_raw_parts(ptr as *mut u8, len, len) }
}

#[no_mangle]
pub fn register(
    signal_ptr: *const u8,
    signal_len: usize,
    filter_ptr: *const u8,
    filter_len: usize,
    stop_loss_ptr: *const u8,
    stop_loss_len: usize,
    exit_ptr: *const u8,
    exit_len: usize,
) -> i32 {
    let signal_buffer = read_from_memory(signal_ptr, signal_len);
    let filter_buffer = read_from_memory(filter_ptr, filter_len);
    let stop_loss_buffer = read_from_memory(stop_loss_ptr, stop_loss_len);
    let exit_buffer = read_from_memory(exit_ptr, exit_len);

    let signal: SignalConfig = serde_json::from_slice(&signal_buffer).unwrap();
    let filter: FilterConfig = serde_json::from_slice(&filter_buffer).unwrap();
    let stop_loss: StopLossConfig = serde_json::from_slice(&stop_loss_buffer).unwrap();
    let exit: ExitConfig = serde_json::from_slice(&exit_buffer).unwrap();

    let mapped_signal = map_to_signal(signal);
    let mapped_filter = map_to_filter(filter);
    let mapped_stoploss = map_to_stoploss(stop_loss);
    let mapped_exit = map_to_exit(exit);

    register_strategy(mapped_signal, mapped_filter, mapped_stoploss, mapped_exit)
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
    create_and_register(
        SignalConfig::Ma3Cross {
            smoothing,
            short_period,
            medium_period,
            long_period,
        },
        FilterConfig::Dumb {
            period: long_period,
        },
        StopLossConfig::Atr {
            period: atr_period,
            multi: atr_factor,
        },
        ExitConfig::Dumb {},
    )
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
    create_and_register(
        SignalConfig::TIICross {
            major_period,
            minor_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_crossrsin(
    rsi_type: f32,
    rsi_period: f32,
    threshold: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::RsiNeutralityCross {
            rsi_type,
            rsi_period,
            threshold,
        },
        FilterConfig::Dumb { period: rsi_period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_rsivma(
    rsi_type: f32,
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::RsiV {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_rsi2ma(
    rsi_type: f32,
    rsi_period: f32,
    lower_barrier: f32,
    upper_barrier: f32,
    smoothing: f32,
    short_period: f32,
    long_period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Rsi2Ma {
            rsi_type,
            rsi_period,
            lower_barrier,
            upper_barrier,
            smoothing,
            short_period,
            long_period,
        },
        FilterConfig::Dumb {
            period: long_period,
        },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_ground(smoothing: f32, period: f32, atr_period: f32, stop_loss_multi: f32) -> i32 {
    create_and_register(
        SignalConfig::Testground { smoothing, period },
        FilterConfig::Dumb { period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_candlet(
    candle: f32,
    smoothing: f32,
    period: f32,
    atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::Trendcandle { candle },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
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
    create_and_register(
        SignalConfig::SnAtr {
            atr_period,
            atr_smoothing_period,
            lower_barrier,
            upper_barrier,
        },
        FilterConfig::Ma { smoothing, period },
        StopLossConfig::Atr {
            period: stop_loss_atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}

#[no_mangle]
pub fn register_supflip(
    atr_period: f32,
    factor: f32,
    rsi_type: f32,
    rsi_period: f32,
    rsi_threshold: f32,
    stop_loss_atr_period: f32,
    stop_loss_multi: f32,
) -> i32 {
    create_and_register(
        SignalConfig::SupFlip { atr_period, factor },
        FilterConfig::Rsi {
            rsi_type,
            period: rsi_period,
            threshold: rsi_threshold,
        },
        StopLossConfig::Atr {
            period: stop_loss_atr_period,
            multi: stop_loss_multi,
        },
        ExitConfig::Dumb {},
    )
}
